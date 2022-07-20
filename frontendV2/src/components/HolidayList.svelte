<script lang="ts">
    export let listName:string
    export let holidayList: string[]
</script>

{#if holidayList.length > 0}
<main>
    <h1>{listName}</h1>
    <ul>
        {#each holidayList as h}
            <li>{h}</li>
        {/each}
    </ul>
</main>
{/if}

<style>
    main {
        background-color: ghostwhite;
		border-color: orangered;
		border-radius: 2em;
		border-style: solid;
		border-width: 1%;
	}
</style>