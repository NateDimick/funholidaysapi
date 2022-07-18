<script lang="ts">
    export let holidayList: string[]
</script>

<main>
    <ul>
        {#each holidayList as h}
            <li>{h}</li>
        {/each}
    </ul>
</main>