# vue_frontend

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).





### Fresh Install

```
rm .\node_modules
```
or
```
rm -rf node_modules
```

```
rm package-lock.json
```

```
npm cache clear --force

npm update

npm i
```





<!-- heroku config:set NODE_ENV=production -->
<!-- heroku config:set NPM_CONFIG_PRODUCTION=false -->
<!-- heroku config:set YARN_PRODUCTION=true -->
<!-- heroku config:unset NODE_MODULES_CACHE -->
<!-- heroku config:set BUILDPACK_TIMEOUT=30 -->

## Licensing

Original openESEA frontend code is licensed under GNU AGPLv3 (`AGPL-3.0-only`); see [LICENSE.txt](LICENSE.txt) and the [repository licensing guide](../../LICENSING.md).

Apache ECharts is a separately licensed dependency under Apache 2.0. See [third-party notices](public/THIRD_PARTY_NOTICES.txt) for the charting dependencies. The files in `public/licenses/` and `public/THIRD_PARTY_NOTICES.txt` are included in standard Vue CLI builds; preserve them when publishing or redistributing those builds.
