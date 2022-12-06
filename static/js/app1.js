const valid = document.body.querySelector('.validator')
const password = document.body.querySelector('#password')

valid.addEventListener('mousedown', function(){
    password.type = 'text'
})

valid.addEventListener('mouseup', function(){
    password.type = 'password'
})