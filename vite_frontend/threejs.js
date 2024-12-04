import {
    BoxGeometry,
    Color,
    Mesh,
    MeshBasicMaterial,
    PerspectiveCamera,
    Scene,
    WebGLRenderer,
} from 'three';

const container = document.querySelector('#scene-container');

const scene = new Scene();
scene.background = new Color('skyblue');

const fov = 35;
const aspect = container.clientWidth / container.clientHeight;
const near = 0.1;
const far = 100;
const camera = new PerspectiveCamera(fov, aspect, near, far);
camera.position.set(0, 0, 10);
const geometry = new BoxGeometry(2, 2, 2);
const material = new MeshBasicMaterial();
const cube = new Mesh(geometry, material);
scene.add(cube);
const renderer = new WebGLRenderer();
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(window.devicePixelRatio);
container.append(renderer.domElement);
renderer.render(scene, camera);