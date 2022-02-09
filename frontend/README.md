# core-ui

> Open Source Admin Template

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report

# run unit tests
npm run unit

# run e2e tests
npm run e2e

# run all tests
npm test

```

# to analyse bundle
`webpack --config build/webpack.prod.conf.js  --json | webpack-bundle-size-analyzer`

# Deployment

- Pushing/merging your changes to `master` branch will trigger deployment to 
https://stage.app.bookedfusion.com/
- Creating tags in master branch will deploy changes to production which can be located in the URL 
https://app.bookedfusion.com/

# Endpoints
1. Production
  - https://app.bookedfusion.com/
2. Staging
  - https://s-app.bookedfusion.com/
  - 
  
Note: To see log files: command `fab awslogs_tail`  
