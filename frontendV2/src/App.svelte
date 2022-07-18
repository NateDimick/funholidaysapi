<script lang="ts">
	import Router from "svelte-spa-router"
	import Docs from "./routes/Docs.svelte";
	import Home from "./routes/Home.svelte";
	import Lookup from "./routes/Lookup.svelte";
	const routes = {
		'/': Home,
		'/docs': Docs,
		'/demo': Lookup
	}
</script>

<main>
	<Router {routes}/>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}
</style>