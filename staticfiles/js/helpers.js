function $all(sel,cb) {
	document.querySelectorAll(sel).forEach(el => cb(el))
}

function formateTime(content) {
	let currentText = content.textContent
	let newText = currentText.split(",")[0]
	let textregx = /([a-z]+)/
	let text = newText.replace(textregx,(el)=> el[0])
	content.textContent = text
}

function formateTimes(selector) {
	$all(selector,formateTime)
}

function eachClick(selector,cb) {
	$all(selector,elelment => {
		elelment.addEventListener("click",ev => cb(elelment))
	})
}

const fileReader = file => new Promise((resolve,reject) => {
	const reader = new FileReader();
	reader.readAsDataURL(file)
	reader.onload = () => resolve(reader.result)
	reader.onerror = error => reject(error)
})

function makeBucttonActive(Selector,cb) {
	let btnSelector = document.querySelector(Selector)
	if(cb() == true) {
		btnSelector.disabled = false	
	} else {
		btnSelector.disabled = true
	}
}

formateTimes(".time")
eachClick("#menu_toggle",menuBtn => {
	let target = $(menuBtn).attr("data-target")
	let menuTarget = document.querySelector(target)
	//let isOpen = imenuTarget.classList.includes("toggle_sidebar")
	menuTarget.classList.toggle("toggle_sidebar")
})


function closeModal(target) {
	let el = document.querySelector(target).getElementsByClassName('t-modal-content')
	$(target).addClass("fade")
	setTimeout(() => {
		$(target).css({ "display" : "none" })
	},700)
}


$(".t-modal").click(function() {
	let target = document.getElementById($(this).attr("id"))
	closeModal(target)
})


eachClick("[data-cancel]",closeBtn => {
	let target = $(closeBtn).attr("data-cancel")
	closeModal(target)
})

function openModal() {
	$("#create_new_list").css({ 'display' : 'block' }).removeClass("fade")
}

eachClick(".slideToggle",btn => {
	if(!btn) return
	let target = $(btn).attr("data-target")
	let data = $(target).toggle(500)
})

function showElement(target) {
	$(target).show()
}

function hideElement(target) {
	$(target).hide()
}

eachClick(".show-el",btn => {
	if(!btn) return
	let target = $(btn).attr("data-target")
	showElement(target)
})

eachClick(".hide-el",btn => {
	if(!btn) return
	let target = $(btn).attr("data-target")
	hideElement(target)
})

let thin = `<svg fill="var(--special-text)" viewBox="0 0 16 16"><path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/></svg>` 

$all('.circle-thin',icon => icon.innerHTML = thin)

