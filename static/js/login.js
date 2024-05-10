const toastTrigger = document.getElementById('liveToastBtn')
const toastLiveExample = document.getElementById('liveToast')

if (toastTrigger) {
  const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)
  toastTrigger.addEventListener('click', () => {
    toastBootstrap.show()
  })
}

document.addEventListener("DOMContentLoaded", function() {
    const inputs = document.querySelectorAll('.fieldUserLogin, .fieldUserPasswd');
    const title = document.querySelector('.mchatTitle');

    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            title.classList.add('hidden-title');
        });
        input.addEventListener('blur', () => {
            title.classList.remove('hidden-title');
        });
    });
});
