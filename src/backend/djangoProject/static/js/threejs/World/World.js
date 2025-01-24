import {createCamera} from "../Components/camera.js";
import {createCube} from "../Components/cube.js";
import {createScene} from "../Components/scene.js";
import {createLights} from "../Components/lights.js";
import {createRenderer} from "../Systems/renderer.js";
import {Resizer} from "../Systems/Resizer.js";
import {Loop} from "../Systems/Loop.js";
import {Paddle} from "../Systems/Paddle.js"
import {createControls} from "../Systems/controls.js";
import {Ball} from "../Systems/Ball.js";
import {BufferGeometry, Group, Line, LineBasicMaterial, Vector3, CameraHelper} from "three";
import {Align, createFont} from "../Components/font.js";
import {loadModel} from "../Components/modelLoader.js";

let camera, renderer, scene, loop, loc, active_paddle, default_paddle;
let local = false;

function degToRad(degrees) {
    return degrees * (Math.PI / 180);
}

class World {
    constructor(container) {
        let lastPart = window.location.toString().split("/");

        lastPart = lastPart.pop() || lastPart.pop();
        const webSocket = new WebSocket("ws://" + window.location.host + "/ws/game/" + lastPart + "/");

        webSocket.onopen = (event) => {
            console.log("WebSocket connection established.");
        };

        webSocket.onclose = (event) => {
            console.warn("WebSocket connection closed:", event);
            // Optionally attempt reconnection
        };

        webSocket.onerror = (error) => {
            console.error("WebSocket error:", error);
        };

        webSocket.onmessage = (event) => {
            const json = JSON.parse(event.data);
            console.log(json);
            if (json['type'] === 'init_ball') {
                this.ball = new Ball(json['x'], json['y'], json['v_x'], json['v_y'], json['speed'], json['radius'], 50, 50);
                loop.updatables.push(this.ball);
                scene.add(this.ball.model);
            } else if (json['type'] === 'client') {
                loc = json['loc'];
                if (this.ball)
                    scene.remove(this.ball.model);
                if (active_paddle) {
                    scene.remove(active_paddle.model);
                    active_paddle = undefined;
                }
                if (default_paddle) {
                    scene.remove(default_paddle.model);
                    default_paddle = undefined;
                }
            } else if (json['type'] === 'local_client') {
                loc = "right";
                local = true;
            } else if (json['type'] === 'init_paddle') {
                console.log(json['name']);
                if (loc === "spectator" && !active_paddle) {
                    let align = Align.Left;
                    if (json['loc'] === "right")
                        align = Align.Right;
                    console.log("active paddle loc = " + json['loc']);
                    active_paddle = new Paddle(json['loc'], json['name'], json['speed'], json['width'], json['size'], false, json['x'], 50, 50, webSocket);
                    createFont(scene, active_paddle.x, 55, -5, active_paddle.name, null, null, align, 7);
                    scene.add(active_paddle.model);
                    loop.updatables.push(active_paddle);
                } else if (loc === json['loc']) {
                    let align = Align.Left;
                    if (loc === "right")
                        align = Align.Right;
                    active_paddle = new Paddle(loc, json['name'], json['speed'], json['width'], json['size'], false, json['x'], 50, 50, webSocket);
                    createFont(scene, active_paddle.x, 55, -5, active_paddle.name, null, null, align, 7);
                    scene.add(active_paddle.model);
                    loop.updatables.push(active_paddle);
                } else {
                    let align = Align.Left;
                    console.log("Default paddle loc = " + json['loc']);
                    default_paddle = new Paddle(json['loc'], json['name'], json['speed'], json['width'], json['size'], false, json['x'], 50, 50, webSocket);
                    if (local)
                        default_paddle.registerLocalInput()
                    if (json['loc'] === "right")
                        align = Align.Right;
                    createFont(scene, default_paddle.x, 55, -5, default_paddle.name, null, null, align, 7);
                    scene.add(default_paddle.model);
                    loop.updatables.push(default_paddle);
                }
            } else if (json['type'] === 'paddle') {
                console.log(active_paddle.location)
                if (active_paddle.location === json['loc']) {
                    active_paddle.y = -json['y'] + 50;
                    console.log("set to " + json['y']);
                } else {
                    default_paddle.y = -json['y'] + 50;
                    console.log("set to " + json['y']);
                }
            } else if (json['type'] === 'ball') {
                if ((json['y'] > 2 && json['y'] < 97) || (json['x'] < 10 || json['x'] > 90))
                    this.ball.collide(json['x'], json['y'], json['v_x'], json['v_y'], json['speed']);
            } else if (json['type'] === 'score') {
                if (json['value'] >= 10) {
                    default_paddle.active = false;
                    active_paddle.active = false;
                    scene.remove(this.ball.model);
                }
                this.ball.collide(json['x'], json['y'], json['v_x'], json['v_y'], json['speed']);
                console.log(active_paddle);
                if (json['loc'] === active_paddle.location)
                    default_paddle.score = json['value'];
                else
                    active_paddle.score = json['value'];

                let mult = -1;
                if (active_paddle.location === "right")
                    mult = 1;
                console.log(active_paddle.score)
                createFont(scene, 30 * mult, 30, 0, Number(active_paddle.score) >= 10 ? active_paddle.score.toString() : "0" + active_paddle.score, fontGroup, fontGroup.children[0]);
                createFont(scene, 30 * -mult, 30, 0, Number(default_paddle.score) >= 10 ? default_paddle.score.toString() : "0" + default_paddle.score, fontGroup, fontGroup.children[1]);
                scene.add(fontGroup);
            } else if (json['type'] === "start_game") {
                active_paddle.active = true;
                active_paddle.registerInput();
            } else if (json['type'] === 'redirect') {
                console.log(window.location.host + json['url']);
                window.location.href = json['url'];
            }
        }


        camera = createCamera();
        scene = createScene();
        renderer = createRenderer();
        loadModel('/static/js/threejs/Models/nowall.glb', (obj) => {
            obj.scale.set(118, 118, 118);
            obj.position.set(0, 0, -5);
            obj.rotation.set(degToRad(90), degToRad(90), 0);
            obj.castShadow = true;
            scene.add(obj);
        });
        const fontGroup = new Group();
        createFont(scene, -30, 30, 0, "00", fontGroup);
        createFont(scene, 30, 30, 0, "00", fontGroup);

        const controls = createControls(camera, renderer.domElement);

        const {ambientLight, light} = createLights();

        loop = new Loop(camera, scene, renderer);
        container.append(renderer.domElement);

        // const top = createCube();
        // const bot = createCube();
        // top.position.set(0, 51, 0);
        // top.scale.set(50, 1, 1);
        // bot.position.set(0, -51, 0);
        // bot.scale.set(50, 1, 1);

        const mat = new LineBasicMaterial({color: 0x0000ff});
        const points = [];
        points.push(new Vector3(-50, -50, 0));
        points.push(new Vector3(50, -50, 0));
        points.push(new Vector3(50, 50, 0));
        points.push(new Vector3(-50, 50, 0));
        points.push(new Vector3(-50, -50, 0));
        points.push(new Vector3(-50 + 3, -50 + 3))
        points.push(new Vector3(50 - 3, -50 + 3, 0));
        points.push(new Vector3(50 - 3, 50 - 3, 0));
        points.push(new Vector3(-50 + 3, 50 - 3, 0));
        points.push(new Vector3(-50 + 3, -50 + 3, 0));

        const geometry = new BufferGeometry().setFromPoints(points);
        const line = new Line(geometry, mat);
        scene.add(line);

        loop.updatables.push(controls);

        scene.add(ambientLight, light, fontGroup);

        this.canvas = renderer.domElement;

        const resizer = new Resizer(container, camera, renderer);
    }

    render() {
        renderer.render(scene, camera);
    }

    start() {
        loop.start();
    }

    stop() {
        loop.stop();
    }
}

export {World};