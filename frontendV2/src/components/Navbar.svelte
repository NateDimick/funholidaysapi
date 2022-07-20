<script lang="ts">
    import NavbarItem from "./NavbarItem.svelte"
    import type { NavItemProp } from "../types"

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
        display: flex;
        flex-direction: row;
        justify-content: space-evenly;
    }
    h1 {
        color: ghostwhite;
    }
</style>