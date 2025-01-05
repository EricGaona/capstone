document.addEventListener("DOMContentLoaded", () => {
    const carouselElement = document.querySelector('#carouselExampleControls');
    const carousel = new bootstrap.Carousel(carouselElement, {
        interval: 25000,  // Auto-slide every 2 seconds
        //   ride: 'carousel' // Automatically start the carousel when the page loads
    });

    // You can also manually control the carousel
    document.querySelector('.carousel-control-prev').addEventListener('click', function () {
        carousel.prev();  // Go to the previous item
    });

    document.querySelector('.carousel-control-next').addEventListener('click', function () {
        carousel.next();  // Go to the next item
    });
});