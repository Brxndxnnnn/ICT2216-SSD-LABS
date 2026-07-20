// Deliberately insecure sample to demonstrate eslint-plugin-security.
// Running `npx eslint test.js` should report the eval-with-expression finding.
// DO NOT ship code like this.

const expression = '1 + 1';
eval(`console.log(${expression})`); // security/detect-eval-with-expression -> error
