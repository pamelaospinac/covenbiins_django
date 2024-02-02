function confirmar_eliminar(url){
    if(confirm("Está seguro de eliminar el registro?")){
        location.href = url;
    }
}

function login(url_django){
    var value = $("[name='csrfmiddlewaretoken']").val();
    $.ajax({
      method: "POST",
      url: url_django,
      data: { email: $("#emailInicio").val(), contrasena: $("#passwordInicio").val(), csrfmiddlewaretoken: value}
    })
    .fail(function( result ) {
        alert("Error: " + result)
    })
    .done(function( result ) {
        if (result == "Malo"){
            alert("Usuario o Contraseña incorrecta")
        }
        else{
            location.href = ""
        }
    });
}