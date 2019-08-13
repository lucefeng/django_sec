function check() {
    if(document.getElementById("pwd").value!=document.getElementById("pwd_check").value)
    {
        document.getElementById("warning").innerHTML= "密码不一致"
    }
    else
    {
        document.getElementById("warning").innerHTML= " "
    }

}

function check_name(){
    axios.get(this.host+"//")

}


