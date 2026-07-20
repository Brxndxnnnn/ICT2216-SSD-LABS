// ESLint 9 flat config with security plugins (Week 8).
// This config targets a plain JS/Node project so it runs without React/Babel.
// For a React project, see the lab PDF's react-oriented example.
//
// Install:
//   npm install "eslint@^9" --save-dev
//   npm install eslint-plugin-security --save-dev
//   npm install eslint-plugin-security-node --save-dev
//   npm install eslint-plugin-no-unsanitized --save-dev
//   npm install @microsoft/eslint-formatter-sarif --save-dev

import { defineConfig } from "eslint/config";
import pluginSecurity from "eslint-plugin-security";
import securityNode from "eslint-plugin-security-node";
import noUnsanitized from "eslint-plugin-no-unsanitized";

export default defineConfig([
  {
    files: ["**/*.{js,mjs,cjs}"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: {
        process: "readonly",
        console: "readonly",
        Buffer: "readonly",
        module: "readonly",
        require: "readonly",
        __dirname: "readonly",
      },
    },
    plugins: {
      security: pluginSecurity,
      "security-node": securityNode,
      "no-unsanitized": noUnsanitized,
    },
    rules: {
      // eslint-plugin-security — common JS security smells
      ...pluginSecurity.configs.recommended.rules,
      "security/detect-eval-with-expression": "error",
      "security/detect-non-literal-fs-filename": "warn",
      "security/detect-child-process": "warn",

      // eslint-plugin-security-node — Node-specific issues (e.g. CRLF/log injection)
      "security-node/detect-crlf": "error",

      // eslint-plugin-no-unsanitized — flags unsafe DOM sinks (XSS)
      ...noUnsanitized.configs.recommended.rules,
    },
  },
  {
    // don't lint dependencies or generated reports
    ignores: ["node_modules/**", "reports/**"],
  },
]);
