window.onload=function() {
  showLoginForm();
}
document.getElementById('registrationForm').addEventListener('submit', function(event) {
    event.preventDefault();
  
    const firstname = document.getElementById('fname').value;
    const lastname = document.getElementById('lname').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    // Create data object to be sent
    const data = {
        "firstName": firstname,
        "lastName":lastname,
        "emailId":email,
        "password": password
    };
  
    // POST request using fetch
    fetch('/registerUser', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
      // Handle response data
      console.log(data);
    })
    .catch(error => {
      // Handle any errors
      console.error('Error:', error);
    });
  });



  document.getElementById('loginform').addEventListener('submit', function(event) {
    event.preventDefault();
  
    
    const email = document.getElementById('usernameForLogin').value;
    const password = document.getElementById('passwordForLogin').value;
    // Create data object to be sent
    const data = {
        
        "userName":email,
        "password": password
    };
  
    // POST request using fetch
    fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
      // Handle response data
      console.log(data);
      if(data.status==0){
        console.log('LOGIN SUCCESS');
        window.location.href="message.html?userId="+data.userId+"&firstName="+data.firstName;
      }else{
        document.getElementById("message-display-span").innerHTML=`<h3>Login Failed!</h3>`;
        console.log('LOGIN FAILED');
      }
    })
    .catch(error => {
      // Handle any errors
      console.error('Error:', error);
    });
  });

  function showForm() 
        {
          var signInForm = document.getElementById("loginform");
          var registerForm = document.getElementById("registrationForm");
          signInForm.classList.add("hidden");
          registerForm.classList.remove("hidden");
          document.getElementById("message-display-span").innerHTML=``;
        }
        function showLoginForm() 
        {
          var signInForm = document.getElementById("loginform");
          var registerForm = document.getElementById("registrationForm");
          signInForm.classList.remove("hidden");
          registerForm.classList.add("hidden");
          document.getElementById("message-display-span").innerHTML=``;
        }
  