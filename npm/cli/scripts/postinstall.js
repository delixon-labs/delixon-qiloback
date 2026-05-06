/* eslint-env node */
/*
 * Lazy native-binary downloader for @delixon/qiloback.
 *
 * On install we map the host (platform + arch) to a release asset in
 * GitHub Releases, fetch it, verify the sha256 against the SHA256SUMS
 * file shipped alongside the binaries, chmod +x, and place it under
 * ../bin/. The wrapper script bin/qiloback then execs the native
 * binary so the user lands at a familiar `qiloback ...` shell.
 *
 * Set NPM_QILOBACK_SKIP_POSTINSTALL=1 to skip the download — useful
 * for CI runners that pre-bake the binary.
 */
const { platform, arch } = process;
const https = require("https");
const crypto = require("crypto");
const {
  createWriteStream,
  chmodSync,
  existsSync,
  mkdirSync,
  readFileSync,
  unlinkSync,
} = require("fs");
const { join } = require("path");

const ASSET_MAP = {
  "win32-x64": "qiloback-cli-win32-x64.exe",
  "linux-x64": "qiloback-cli-linux-x64",
  "linux-arm64": "qiloback-cli-linux-arm64",
  "darwin-x64": "qiloback-cli-darwin-x64",
  "darwin-arm64": "qiloback-cli-darwin-arm64",
};

const key = `${platform}-${arch}`;
const asset = ASSET_MAP[key];

if (!asset) {
  console.error(`@delixon/qiloback: unsupported platform (${key})`);
  console.error(
    "Supported: win32-x64, linux-x64, linux-arm64, darwin-x64, darwin-arm64",
  );
  process.exit(1);
}

if (process.env.NPM_QILOBACK_SKIP_POSTINSTALL === "1") {
  process.exit(0);
}

const pkg = require("../package.json");
const version = pkg.version;
const releaseBase = `https://github.com/delixon-labs/delixon-qiloback/releases/download/v${version}`;
const binaryUrl = `${releaseBase}/${asset}`;
const checksumsUrl = `${releaseBase}/SHA256SUMS`;
const binaryName = platform === "win32" ? "qiloback.exe" : "qiloback";
const binDir = join(__dirname, "..", "bin");
const destPath = join(binDir, binaryName);

if (!existsSync(binDir)) {
  mkdirSync(binDir, { recursive: true });
}

function download(url, dest, maxRedirects) {
  return new Promise((resolve, reject) => {
    function attempt(current, remaining) {
      if (remaining < 0) {
        return reject(new Error("too many redirects"));
      }
      https
        .get(current, (res) => {
          if (
            res.statusCode >= 300 &&
            res.statusCode < 400 &&
            res.headers.location
          ) {
            return attempt(res.headers.location, remaining - 1);
          }
          if (res.statusCode !== 200) {
            return reject(new Error(`HTTP ${res.statusCode} fetching ${current}`));
          }
          const file = createWriteStream(dest);
          res.pipe(file);
          file.on("finish", () => file.close(() => resolve()));
          file.on("error", (err) => {
            try {
              unlinkSync(dest);
            } catch {
              /* ignore */
            }
            reject(err);
          });
        })
        .on("error", reject);
    }
    attempt(url, maxRedirects);
  });
}

function fetchText(url, maxRedirects) {
  return new Promise((resolve, reject) => {
    function attempt(current, remaining) {
      if (remaining < 0) return reject(new Error("too many redirects"));
      https
        .get(current, (res) => {
          if (
            res.statusCode >= 300 &&
            res.statusCode < 400 &&
            res.headers.location
          ) {
            return attempt(res.headers.location, remaining - 1);
          }
          if (res.statusCode === 404) return resolve(null);
          if (res.statusCode !== 200) {
            return reject(new Error(`HTTP ${res.statusCode} fetching ${current}`));
          }
          const chunks = [];
          res.on("data", (c) => chunks.push(c));
          res.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
          res.on("error", reject);
        })
        .on("error", reject);
    }
    attempt(url, maxRedirects);
  });
}

function sha256OfFile(path) {
  const hash = crypto.createHash("sha256");
  hash.update(readFileSync(path));
  return hash.digest("hex");
}

(async () => {
  try {
    console.log(`@delixon/qiloback: downloading ${asset} for v${version}`);
    await download(binaryUrl, destPath, 10);

    const sums = await fetchText(checksumsUrl, 10);
    if (sums) {
      const expected = sums
        .split(/\r?\n/)
        .map((line) => line.trim())
        .find((line) => line.endsWith(asset));
      if (expected) {
        const expectedHash = expected.split(/\s+/)[0].toLowerCase();
        const actualHash = sha256OfFile(destPath).toLowerCase();
        if (expectedHash !== actualHash) {
          try {
            unlinkSync(destPath);
          } catch {
            /* ignore */
          }
          console.error(
            `@delixon/qiloback: sha256 mismatch — expected ${expectedHash}, got ${actualHash}`,
          );
          process.exit(2);
        }
      } else {
        console.warn(
          `@delixon/qiloback: ${asset} not listed in SHA256SUMS — proceeding without verification`,
        );
      }
    } else {
      console.warn(
        "@delixon/qiloback: SHA256SUMS not published for this release — proceeding without verification",
      );
    }

    if (platform !== "win32") {
      chmodSync(destPath, 0o755);
    }

    console.log(`@delixon/qiloback: installed at ${destPath}`);
  } catch (err) {
    console.error("@delixon/qiloback: postinstall failed:", err.message || err);
    console.error(
      "Set NPM_QILOBACK_SKIP_POSTINSTALL=1 to skip the download (advanced).",
    );
    process.exit(1);
  }
})();
