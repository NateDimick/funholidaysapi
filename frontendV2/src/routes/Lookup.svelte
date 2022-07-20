<script lang="ts">
    import { onMount } from "svelte";
    import { querystring } from "svelte-spa-router";
    import HolidayList from "../components/HolidayList.svelte";
    import Navbar from "../components/Navbar.svelte";
import { QueryParams } from "../types";

    const navbarInfo = {
        pageName: "API Reference",
        itemProps: [
            {
                link: "/#",
                linkText: "Go Home",
                mainText: ""
            }
        ]
    }

    let holidayList: string[] = []
    let domain: string = ""
    let shareLink: string = ""

    let keyword: string
    let keydate: string
    let listName: string = ""

    let searchMode: boolean = true


    function dateQuery() {
        let date = keydate.split("-");
        try {
            let url = `/api/date/${date[1]}/${date[2]}`
            console.log(url);
        } catch (error) {
            console.log('bad date');
            return false;
        }
        let url = `/api/date/${date[1]}/${date[2]}`
        fetch(url)
        .then(response => response.json())
        .then(data => data.holidays)
        .then(holidays => {
            // insert new results
            let temp: string[] = []
            holidays.forEach(element => {
                temp.push(`${date[1]}/${date[2]}: ${element}`)
            })
            holidayList = temp
            shareLink = `${domain}/#/demo?dt=${keydate}`
        });
        listName = `holidays on ${date[1]}/${date[2]}`
    }

    function wordQuery() {
        let url = `/api/search/${encodeURIComponent(keyword)}`;
        fetch(url)
        .then(response => response.json())
        .then(data => {
            if (Object.keys(data).length === 0) {
                holidayList = [`No results for "${keyword}"`]
            }
            let temp: string[] = []
            Object.keys(data).forEach(month => {
                Object.keys(data[month]).forEach(day => {
                    data[month][day].forEach(holiday => {
                        temp.push(`${month}/${day}: ${holiday}`)
                    })
                    
                })
            })
            holidayList = temp
            let linkWord = encodeURIComponent(keyword);
            shareLink = `${domain}/#/demo?kw=${linkWord}`
        });
        listName = `${keyword} Holidays`
    }

    onMount(() => {
        domain = document.URL.split("/#/")[0]
        let query = QueryParams.from($querystring)
        if (query.has("kw")) {
            searchMode = true
            keyword = query.get("kw")
            wordQuery()
        }
        if (query.has("dt")) {
            searchMode = false
            keydate = query.get("dt")
            dateQuery()
        }
    })
</script>

<main>
    <Navbar {...navbarInfo}/>
    <div id="toggle">
        <button on:click={() => searchMode = true}>Keyword Search</button>
        <button on:click={() => searchMode = false}>Date Search</button>
    </div>
    <section>
        <div id="word-search" class="field" hidden={!searchMode}>
            <!-- This div will be a form to find holidays based on keyword similarity -->
            <label for="keyword">Holiday Keyword</label>
            <input type="text" name="keyword" id="keyword" placeholder="pizza, flower, etc" bind:value={keyword}>
            <button id="keyword-search" on:click={wordQuery}>Find Holidays</button>
        </div>
        <div id="date-search" class="field" hidden={searchMode}>
            <!-- This div will be a form to find holidays based on the date -->
            <label for="date">Find Holidays by Date</label>
            <input type="date" name="date" id="date" on:change={dateQuery} bind:value={keydate}>   
        </div>
    </section>
    <HolidayList {holidayList} {listName}/>
    {#if shareLink}
        <section id="bottom">
            <h2>
                Share these results <a href={shareLink}>{shareLink}</a>
            </h2>
        </section>
    {/if}
    
</main>

<style>
    main {
		width: 60%;
		margin: 0% 18%;
	}
    section {
        background-color: ghostwhite;
		border-color: orangered;
		border-radius: 0 0 2em 2em;
		border-style: solid;
		border-width: 3px;
		padding: 2%
    }
    #bottom {
        border-radius:  2em;
    }
    #toggle {
        display: flex;
    }
    #toggle > button {
        flex: 1 1 0px;
        margin: 0;
        border-radius: 2em 2em 0 0;
        border-style: solid;
		border-width: 3px 3px 0px 3px;
        border-color: orangered;
        background-color: ghostwhite;
    }
    #toggle > button:hover {
        background-color: dodgerblue;
    }
</style>