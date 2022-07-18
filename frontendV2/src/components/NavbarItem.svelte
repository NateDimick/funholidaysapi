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