let link = document.querySelector("#cate")
let list = document.querySelector("#cat")
let arw = document.querySelector("#arrow")

link.addEventListener("mouseover", () => {
    list.style.visibility = "visible"
    link.style.color = "#ff6905"
    arw.style.transform = "rotate(-90deg)"
})

link.addEventListener("mouseout", () => {
    list.style.visibility = "hidden"
    link.style.color = "white"
    arw.style.transform = "rotate(0deg)"
})

list.addEventListener("mouseover", () => {
    list.style.visibility = "visible"
    arw.style.transform = "rotate(-90deg)"
})

list.addEventListener("mouseout", () => {
    list.style.visibility = "hidden"
    arw.style.transform = "rotate(0deg)"
})