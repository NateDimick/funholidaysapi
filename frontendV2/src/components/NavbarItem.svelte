<script lang="ts">
    export let link: string
    export let linkText: string
    export let mainText: string
</script>

<main>
    <h1>{mainText}</h1>
    <h2>
        <a href={link}>{linkText}</a>
    </h2>
</main>

<style>
    main {
        background-color: ghostwhite;
        border-color: orangered;
        border-radius: 2em;
        border-style: solid;
        border-width: 3px;
        padding: 1%;
        flex: 1 1 0px;
        vertical-align:middle;
    }
</style>