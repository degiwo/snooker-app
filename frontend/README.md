# Snooker frontend

Initialized with `npx @angular/cli@latest new snooker_frontend --directory frontend --routing --style=scss --ssr=false --skip-git`.
This project was generated using [Angular CLI](https://github.com/angular/angular-cli) version 22.2.5.

## Project structure

```text
src/app
  core/layout/          App frame: Shell (header, main, nav) and Nav component
  core/navigation/      Title strategy, nav items derived from routes
  features/             One folder per page
public/icons/           SVG icons used by <mat-icon svgIcon="...">
```

## How to

### Add a page

1. Create `src/app/features/<name>/<name>.ts` with `export default class`.
2. Add a route to the `children` of the Shell route in `src/app/app.routes.ts`:
   ```ts
   {
    path: '<name>',
    title: '<Title>',  // browser tab, page heading and nav label
    loadComponent: () => import('./features/<name>/<name>'),
    data: { nav: { icon: '<icon>' } satisfies RouteNavData },  // omit to hide from nav
   },
   ```
   Routes outside the Shell's `children` render without header and navigation.

### Add an icon

Copy both variants (<name>.svg and <name>-fill.svg) from
`node_modules/@material-symbols/svg-400/outlined/` into `public/icons/`.

## Commands

### Install dependencies

```sh
npm install
```

### Lint and format

```sh
npm run format
npm run lint
```

### Development server

```sh
npm run start
```

### Generate new component

```sh
npx ng generate component component-name
```

### Building

```sh
npm run build
```

### Running unit tests

```sh
npm run test
```
