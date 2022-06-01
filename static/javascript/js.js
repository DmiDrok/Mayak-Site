//Функция для выпадающих списков
function list(){
	//Алгоритм для выпадающих списков
	let menu = document.querySelector("#dots_header");
		menuList = document.querySelector("#menu_social")
		navLink = document.querySelector(".nav_element");
		navServices = document.querySelector("#services_menu");
		burgerBlock = document.querySelector("#burger_mobile");
		burgerList = document.querySelector('.burger_list');
	//Для трёхточечного меню
	menu.addEventListener("mouseover", function(){
		menuList.style.display = "block";
	})

	menu.addEventListener("mouseout", function(){
		menuList.style.display = "none";
	})

	//Для списка услуг
	navLink.addEventListener("mouseover", function(){
		navServices.style.display = "block";
	})

	navLink.addEventListener("mouseout", function(){
		navServices.style.display = "none"
	})

	//Для меню мобильных устройств
	burgerBlock.addEventListener("mouseover", function(){
		burgerList.style.display = "block";
	})

	burgerBlock.addEventListener("mouseout", function(){
		burgerList.style.display = "none";
	})
}

list()

//Слайдер третьего блока
try{
	function sliderFect(){
	const sliderLineThird = document.querySelector('.container_line');
	sliderLineThird.style.width = document.querySelector(".wrapper_third .container_line .block").offsetWidth * document.querySelectorAll(".wrapper_third .container_line .block").length + "px";
	const MAX = Number(sliderLineThird.clientWidth) - Number(document.querySelector(".wrapper_third .container_line .block").clientWidth)
	const MIN = 0;

	let leftOff = 0;
		next = document.querySelector('#next');
		prev = document.querySelector('#prev');

	next.addEventListener("click", function(){
		leftOff = leftOff + document.querySelector(".wrapper_third .container_line .block").offsetWidth;
		if(leftOff > MAX){
			leftOff = MIN;
		}
		sliderLineThird.style.left = -leftOff + "px";
	})

	 prev.addEventListener("click", function(){
	 	leftOff = leftOff - document.querySelector(".wrapper_third .container_line .block").offsetWidth;
	 	if(leftOff < MIN){
	 		leftOff = MAX;
	 	}
	 	sliderLineThird.style.left = -leftOff + "px";
	})

	}
sliderFect()
}catch(err){
	console.warn("Слайдер третьего блока не обнаружен.")
}

try{
//Слайдер первого блока
const sliderWrapFirst = document.querySelector('.slider');
const sliderLine = document.querySelector('.slider_line');

let firstButton = document.querySelector("#first_button_bar");
let secondButton = document.querySelector("#second_button_bar");
let btn_args = [firstButton, secondButton];

function saveOne(btn_args, save_btn){

	for (let i=0; i<btn_args.length; i++) {
		if (btn_args[i] != save_btn){
			btn_args[i].classList.remove("active");
		}

		save_btn.classList.add("active");
	}
}

firstButton.classList.add("active");

//Основной код слайдера
function sliderScroll(){
	firstButton.addEventListener("click", function(){
		sliderLine.style.left = document.querySelector(".slider_element").offsetWidth - document.querySelector(".slider_element").offsetWidth; + "px";
		saveOne(btn_args, firstButton);
	})
	secondButton.addEventListener("click", function(){
		sliderLine.style.left = -document.querySelector(".slider_element").offsetWidth + "px";
		saveOne(btn_args, secondButton);
	})
}

// function sliderAuto(){
// 	//Число смещения для автопрокрутки
// 	let numberOff = 0;
// 		leftOff = 0;
// 	//Проверка разрешения монитора
// 	let monitor = setInterval(function monitorXmonitor(){
// 		if(window.screen.width < 420){
// 			numberOff = 750;
// 		}else if(window.screen.width < 1600){
// 			numberOff = 660;
// 		}else if(window.screen.width >= 1600){
// 			numberOff = 850;
// 		}
// 	}, 1000)

// 	//Автопрокрутка слайдера на первом блоке
// 	let autoscroll = setInterval(function forX(){
// 		leftOff = leftOff + numberOff;
// 		//Анимация кнопок
// 		if(leftOff == 0){
// 			firstButton.classList.add("active");
// 			secondButton.classList.remove("active");
// 		}else if(leftOff == numberOff){
// 			firstButton.classList.remove("active");
// 			secondButton.classList.add("active");
// 		}
// 		//Возвращение слайдера на первый блок
// 		sliderLine.style.left = -leftOff + "px";
// 		if(leftOff >= numberOff){
// 			leftOff = -numberOff;
// 		}
// 	}, 15000)

// 	//Сброс таймера по нажатию 
// 	firstButton.addEventListener("click", function(){
// 		clearInterval(autoscroll)
// 		console.log("Интервал Очищен!")
// 	})
// }

sliderScroll()
// sliderAuto()
}catch(err){
	console.warn("Слайдер первого блока не обнаружен")
}
/////Код ПопАпа
const popupActive = document.querySelector(".telefon_children");

let popupWindow = document.querySelector("#popup");
let popupContent = document.querySelector(".popup_content");
let close = document.querySelector("#close");
	//Код вызова
	popupActive.addEventListener("click", function(){
		popupWindow.style.top = "0";
		popupWindow.style.left = "0";
		document.body.style.overflowY = "hidden"
	})
	//Код закрытия
	close.addEventListener("click", function(){
		popupWindow.style.top = "";
		document.body.style.overflowY = "scroll";
	})
	window.onclick = function(event){
		if(event.target == popup){
			popupWindow.style.position = "";
			popupWindow.style.top = "";
			document.body.style.overflowY = "scroll";
		}
	}


//Прогрузка блоков на странице с отзывами(Юристы)
if(window.screen.width > 1024){
	try{
	let buttonShow = document.querySelector("#button_load_more button");


		buttonShow.addEventListener("click", function(){
			let blocks = document.querySelectorAll(".hidden")
			for(let i = 0; i < 3 && i < blocks.length; i = i + 1){
				blocks[i].classList.remove("hidden");
			}

			if(document.querySelectorAll(".hidden").length == 0){
				buttonShow.style.display = "none";
			}
		})
	}catch(err){
		console.warn("Блок с отзывами не обнаружен")
	}
}else{
	try{
	let buttonShow = document.querySelector("#button_load_more button");


		buttonShow.addEventListener("click", function(){
			let blocks = document.querySelectorAll(".hidden")

			for(let i = 0; i < 2 && i < blocks.length; i = i + 1){
				blocks[i].classList.remove("hidden");
			}

			if(document.querySelectorAll(".hidden").length == 0){
				buttonShow.style.display = "none";
			}
		})
	}catch(err){
		console.warn("Блок с отзывами не обнаружен")
	}
}
//Прогрузка блоков на странице психологической помощи
function psihoLoad(){
try{
	if(window.screen.width > 420){
		let buttonDisplay = document.querySelector(".more");

		buttonDisplay.addEventListener("click", function(){
			let blocksPsihologiya = document.querySelectorAll(".hide");

			for(let i = 0; i < 3 && i < blocksPsihologiya.length; i++){
				blocksPsihologiya[i].classList.remove("hide");
			}

			if(document.querySelectorAll(".hide").length == 0){
				buttonDisplay.style.display = "none";
			}
		})
}else if(window.screen.width <= 420){
	let blocksPsiho = document.querySelectorAll(".psiholog__wrapper_third .container .block");

	for(let el = 2; el < 3 && el < blocksPsiho.length; el++ ){
		blocksPsiho[el].classList.add("hide");
	}

	let buttonDisplay = document.querySelector(".more");

	buttonDisplay.addEventListener("click", function(){
		let blocksPsihologiya = document.querySelectorAll(".hide");

		for(let i = 0; i < 2 && i < blocksPsihologiya.length; i++){
			blocksPsihologiya[i].classList.remove("hide");
		}

		if(document.querySelectorAll(".hide").length == 0){
			buttonDisplay.style.display = "none";
		}
	})
}
}catch(err){
	console.warn("Не психологическая помощь")
}
}
psihoLoad()
//Попапы на странице Школы Танцев
function popDanceFunc(){
	const dancePop = document.querySelectorAll(".dance_popup");
		popWaltz = document.querySelector(".pop_waltz");
		popSalza = document.querySelector(".pop_salza");
		popTango = document.querySelector(".pop_tango");
		popYoga = document.querySelector(".pop_yoga");

	let	closeDance = document.querySelector(".dance_close")
		closeWaltz = document.querySelector(".waltz_close");
		closeSalza = document.querySelector(".salza_close")
		closeTango = document.querySelector(".tango_close")
		closeYoga = document.querySelector(".yoga_close")

	let buttonPop = document.querySelectorAll(".dance_pop");
		buttonWaltz = document.querySelector(".waltz");
		buttonSalza = document.querySelector(".salza");
		buttonTango = document.querySelector(".tango");
		buttonYoga = document.querySelector(".yoga");

		//Общее
		//Вальс
		buttonWaltz.addEventListener("click", function(){
			popWaltz.style.position = "fixed";
			popWaltz.style.top = "0";

			document.body.style.overflowY = "hidden";
		})

		closeWaltz.addEventListener("click", function(){
			popWaltz.style.position = "";
			popWaltz.style.top = "";

			document.body.style.overflowY = "scroll";
		})

		window.addEventListener("click", function(event){
			if(popWaltz.style.position = "fixed" && event.target == popWaltz){
				popWaltz.style.position = "";
				popWaltz.style.top = "";

				document.body.style.overflowY = "scroll";
			}
		})
		//Сальса
		buttonSalza.addEventListener("click", function(){
			popSalza.style.position = "fixed";
			popSalza.style.top = "0";

			document.body.style.overflow = "hidden";
		})

		closeSalza.addEventListener("click", function(){
			popSalza.style.position = "";
			popSalza.style.top = "";

			document.body.style.overflowY = "scroll";
		})

		window.addEventListener("click", function(event){
			if(popSalza && event.target == popSalza){
				popSalza.style.position = "";
				popSalza.style.top = "";

				document.body.style.overflowY = "scroll";
			}
		})
		//Танго
		buttonTango.addEventListener("click", function(){
			popTango.style.position = "fixed";
			popTango.style.top = "0";

			document.body.style.overflowY = "hidden";
		})

		closeTango.addEventListener("click", function(){
			popTango.style.position = "";
			popTango.style.top = "";

			document.body.style.overflowY = "scroll";
		})

		window.addEventListener("click", function(event){
			if(popTango && event.target == popTango){
				popTango.style.position = "";
				popTango.style.top = "";

				document.body.style.overflowY = "scroll";
			}
		})
		//Йога
		buttonYoga.addEventListener("click", function(){
			popYoga.style.position = "fixed";
			popYoga.style.top = "0";

			document.body.style.overflow = "hidden";
		})

		closeYoga.addEventListener("click", function(){
			popYoga.style.position = "";
			popYoga.style.top = "";

			document.body.style.overflowY = "scroll";
		})

		window.addEventListener("click", function(event){
			if(popYoga && event.target == popYoga){
				popYoga.style.position = "";
				popYoga.style.top = "";

				document.body.style.overflowY = "scroll";
			}
		})
}
try{
	popDanceFunc();
}catch(err){
	
}