# Lakehouse Web Interface

This template should help get you started developing with Vue 3 in Vite. Installing NodeJs is required to set up the web interface.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) to make the TypeScript language service aware of `.vue` types.

## Customize basic interface configs

1. Change the basic configs by changing the `ui.json` file located at `./src/assets/configs`.

2. To include background and logo images, insert the images into the folder `./src/assets/img` and change the image names in the config `file ui.json`

3. To change the browser's tab's icon, insert your custom icon file (.ico) into the folder `./public` after renaming it of `favicon.ico`

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```
