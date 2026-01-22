// 1. Fundo de Rede Neural Otimizado
const canvas = document.getElementById('neural-canvas');
const ctx = canvas.getContext('2d');

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

let particles = [];
class Particle {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = 1.5;
        this.speedX = Math.random() * 1 - 0.5;
        this.speedY = Math.random() * 1 - 0.5;
    }
    update() {
        this.x += this.speedX;
        this.y += this.speedY;
        if (this.x > canvas.width || this.x < 0) this.speedX *= -1;
        if (this.y > canvas.height || this.y < 0) this.speedY *= -1;
    }
    draw() {
        ctx.fillStyle = 'rgba(0, 245, 255, 0.5)'; // Cyan neon suave
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

function initParticles() {
    particles = [];
    for (let i = 0; i < 100; i++) particles.push(new Particle());
}

function connect() {
    for (let a = 0; a < particles.length; a++) {
        for (let b = a; b < particles.length; b++) {
            let distance = ((particles[a].x - particles[b].x) ** 2) + ((particles[a].y - particles[b].y) ** 2);
            if (distance < 12000) {
                ctx.strokeStyle = `rgba(41, 98, 255, ${1 - distance/12000})`;
                ctx.lineWidth = 0.5;
                ctx.beginPath();
                ctx.moveTo(particles[a].x, particles[a].y);
                ctx.lineTo(particles[b].x, particles[b].y);
                ctx.stroke();
            }
        }
    }
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => { p.update(); p.draw(); });
    connect();
    requestAnimationFrame(animate);
}

initParticles();
animate();

gsap.registerPlugin(ScrollTrigger);

gsap.from(".reveal-text", {
    y: 50,
    opacity: 0,
    duration: 1.2,
    ease: "expo.out",
    delay: 0.5
});

gsap.from(".reveal-tagline", {
    letterSpacing: "10px",
    opacity: 0,
    duration: 1.5,
    ease: "power3.out"
});

document.querySelectorAll(".stat-value").forEach(val => {
    const target = parseInt(val.getAttribute("data-target"));
    ScrollTrigger.create({
        trigger: val,
        start: "top 90%",
        onEnter: () => {
            let obj = { count: 0 };
            gsap.to(obj, {
                count: target,
                duration: 3,
                ease: "power3.out",
                onUpdate: () => val.innerText = Math.floor(obj.count) + "+"
            });
        }
    });
});