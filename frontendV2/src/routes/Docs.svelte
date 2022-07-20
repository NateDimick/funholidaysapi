<script lang="ts">
    import { onMount } from "svelte";
    import Navbar from "../components/Navbar.svelte";

    const navbarInfo = {
        pageName: "API Reference",
        itemProps: [
            {
                link: "/#",
                linkText: "Go Home",
                mainText: ""
            },
            {
                link: "https://github.com/NateDimick/funholidaysapi",
                linkText: "See the Project on Github",
                mainText: ""
            }
        ]
    }

    let docs: string = ""

    onMount(() => {
        const url = "/raw-docs"
        fetch(url).then(resp => {
            return resp.text()
        }).then(respText => {
            docs = respText
        })
    })

</script>

<main>
    <Navbar {...navbarInfo}/>
    <div>
        {@html docs}
    </div>
</main>

<style>
    main {
		width: 60%;
		margin: 0% 18%;
	}
    div {
        background-color: ghostwhite;
		border-color: orangered;
		border-radius: 2em;
		border-style: solid;
		border-width: 3px;
		padding: 2%
    }
</style>