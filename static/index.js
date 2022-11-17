const API = 'http://195.2.79.3:443/'
let button = document.getElementById('export')

async function getFileUrl() {
    let fileUrl = await fetch(API + 'convert_tables')

    return await fileUrl.text()
}

button.addEventListener("click", async () => {
    let url = await getFileUrl()
    console.log(url)

    window.location = API + url
})
let button1 = document.getElementById('export1')

async function getFileUrl1() {
    let fileUrl = await fetch(API + 'get_all_subsrcibes')

    return await fileUrl.text()
}

button1.addEventListener("click", async () => {
    let url = await getFileUrl1()
    console.log(url)

    window.location = API + url
})