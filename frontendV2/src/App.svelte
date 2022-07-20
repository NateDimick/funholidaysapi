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