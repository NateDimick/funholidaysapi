<script lang="ts">
    import NavbarItem from "./NavbarItem.svelte"
    import { NavItemProp } from "../types"

    export let pageName: string
    export let itemProps: NavItemProp[]
</script>

<main>
    <h1>{pageName}</h1>
    <div>
        {#each itemProps as p}
            <NavbarItem {...p}/>
        {/each}
    </div>
</main>

<style>
    div {
        flex: content;
    }
</style>