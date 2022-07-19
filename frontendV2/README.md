# Frontend V2

This is a Svelte frontend based on the default @svelte/template (which is apparently not officially supported/maintained anymore with the release of sveltekit, but this doesn't use sveltekit so who cares?)

## Using The front end

Obviously start with `npm install`, then `npm run build` to compile in to /public

`npm run dev` and `npm run start` are probably broken because `public/index.html` has been edited to find it's scripts and styles in the `/assets` path which is where they are when the backend is serving this content.

## One last note

See the readme in the repository root for information about `svelte-spa-router` which is used to turn this in to a single-page application.
