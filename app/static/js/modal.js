const modal = document.querySelector('.modal-detalles');
const closeModalBtn = document.getElementById('close-modal-btn');

const viewProduct = ({ id }) => {
    console.log(id);
    modal.style.display = 'flex';
};

const closeModal = () => {
    console.log('Cerrando modal');
    modal.style.display = 'none';
};

if (closeModalBtn) {
    closeModalBtn.addEventListener('click', closeModal);
}

window.addEventListener('click', (event) => {
    if (event.target === modal) {
        closeModal();
    }
});