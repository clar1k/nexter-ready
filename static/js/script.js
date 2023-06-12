const btnLogin = document.querySelector(".login")
const btnReg = document.querySelector(".reg")
const userLog = document.querySelector(".user--login")
const userReg = document.querySelector(".user--register")
const btnClose1 = document.querySelectorAll(".btn1")
const btnClose2 = document.querySelectorAll(".btn2")
btnLogin.addEventListener("click",function(e){
    userLog.classList.toggle("hidden")
})
btnReg.addEventListener("click",function(e){
    userReg.classList.toggle("hidden")
})


btnClose2.forEach(el=>el.addEventListener("click",function(e){
    userLog.classList.toggle("hidden")
    // userReg.classList.add("hidden")
    // userLog.classList.toggle("hidden")
}))
btnClose1.forEach(el=>el.addEventListener("click",function(e){
    userReg.classList.toggle("hidden")
    // userReg.classList.add("hidden")
    // userLog.classList.toggle("hidden")
}))

