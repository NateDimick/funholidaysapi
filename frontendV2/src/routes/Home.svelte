<script lang="ts">
    import { onMount } from "svelte";
import HolidayList from "../components/HolidayList.svelte";
    import Navbar from "../components/Navbar.svelte";

    const navbarInfo = {
        pageName: "Fun Holidays!",
        itemProps: [
            {
                link: "/#/docs",
                linkText: "Read The API Docs",
                mainText: " Need Fun Holiday Info?"
            },
            {
                link: "/#/demo",
                linkText: "Use the Interactive Lookup Tool",
                mainText: "Not Interested in the API?"
            }
        ]
    }

    let holidayList: string[] = []

    onMount(() => {
        const url = "/api/today";
        fetch(url)
        .then(response => response.json())
        .then(data => {
            let temp: string[] = []
            data.holidays.forEach(holiday => {
                temp.push(`${data.month}/${data.day}: ${holiday}`)
            })
            holidayList = temp
        })
    })

</script>

<main>
    <Navbar {...navbarInfo}/>
    <section>
        <div>
            <p>
                You've probably seen things like "National Donut Day" or "Talk Like a Pirate Day" on social media before. Have you ever wondered what weird holidays it is today (or any day) and also wanted a convenient API to help you with that? Look no further than here, the Fun Holidays API!
            </p>
        </div>
    </section>
    <HolidayList {holidayList} listName={"Today's Holidays"}/>
</main>

<style>
    main {
		width: 60%;
		margin: 0% 18%;
		
	}
    section {
        background-color: ghostwhite;
		border-color: orangered;
		border-radius: 2em;
		border-style: solid;
		border-width: 3px;
		padding: 2%
    }
</style>