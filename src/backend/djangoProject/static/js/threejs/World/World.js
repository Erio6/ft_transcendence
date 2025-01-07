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
import {BufferGeometry, Group, Line, LineBasicMaterial, Vector3} from "three";
import {Align, createFont} from "../Components/font.js";

let camera, renderer, scene, loop, loc, active_paddle, default_paddle;

class World {
    constructor(container) {
        let lastPart = window.location.toString().split("/");

        lastPart = lastPart.pop() || lastPart.pop();
        const webSocket = new WebSocket("ws://localhost:8000/ws/game/" + lastPart + "/");

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
            }
            else if (json['type'] === 'client') {
                loc = json['loc'];
            }
            else if (json['type'] === 'init_paddle') {
                console.log(json['name']);
                if (loc === json['loc']) {
                    let align = Align.Left;
                    if (loc === "right")
                        align = Align.Right;
                    active_paddle = new Paddle(loc, json['name'], json['speed'], json['width'], json['size'], true, json['x'], 50, 50, webSocket);
                    createFont(scene, active_paddle.x, 55, -5, active_paddle.name, null, null, align, 7);
                    scene.add(active_paddle.model);
                    loop.updatables.push(active_paddle);
                }
                else {
                    let align = Align.Left;
                    default_paddle = new Paddle(json['loc'], json['name'], json['speed'], json['width'], json['size'], false, json['x'], 50, 50, webSocket);
                    if (json['loc'] === "right")
                        align = Align.Right;
                    createFont(scene, default_paddle.x, 55, -5, default_paddle.name, null, null, align, 7);
                    scene.add(default_paddle.model);
                    loop.updatables.push(default_paddle);
                }
            }
            else if (json['type'] === 'paddle') {
                console.log(json['loc'])
                if (loc === json['loc']) {
                    active_paddle.y = -json['y'] + 50;
                    console.log("set to " + json['y']);
                }
                else {
                    default_paddle.y = -json['y'] + 50;
                    console.log("set to " + json['y']);
                }
            }
            else if (json['type'] === 'ball') {
                if (json['y'] > 2 && json['y'] < 97)
                    this.ball.collide(json['x'], json['y'], json['v_x'], json['v_y'], json['speed']);
            }
            else if (json['type'] === 'score') {
                if (json['value'] >= 10) {
                    default_paddle.active = false;
                    active_paddle.active = false;
                    scene.remove(this.ball.model);
                }
                this.ball.collide(json['x'], json['y'], json['v_x'], json['v_y'], json['speed']);
                if (json['loc'] === active_paddle.location)
                    default_paddle.score = json['value'];
                else
                    active_paddle.score = json['value'];

                // scene.remove(fontGroup.children);
                // const children = [...fontGroup.children];
                // children.forEach((child) => {
                //
                //     // If the child has geometry and material, dispose of them
                //     if (child.geometry) child.geometry.dispose();
                //     if (child.material) {
                //         if (Array.isArray(child.material)) {
                //             child.material.forEach((mat) => mat.dispose());
                //         }
                //         else {
                //             child.material.dispose();
                //         }
                //     }
                //     // Remove the child from the group
                //     fontGroup.remove(child);
                //     // child.removeFromParent();
                //     // scene.remove(child);
                // });
                let mult = -1;
                if (active_paddle.location === "right")
                    mult = 1;

                createFont(scene, 30 * mult, 30, -5, Number(active_paddle.score) >= 10 ? active_paddle.score.toString() : "0" + active_paddle.score, fontGroup, fontGroup.children[0]);
                createFont(scene, 30 * -mult, 30, -5, Number(default_paddle.score) >= 10 ? default_paddle.score.toString() : "0" + default_paddle.score, fontGroup, fontGroup.children[1]);
                scene.add(fontGroup);
            }
        }


        camera = createCamera();
        scene = createScene();
        renderer = createRenderer();
        const fontGroup = new Group();
        createFont(scene, -30, 30, -5, "00", fontGroup);
        createFont(scene, 30, 30, -5, "00", fontGroup);

        const controls = createControls(camera, renderer.domElement);

        const top = createCube();
        const bot = createCube();
        // const paddleLeft = createCube();
        // const paddleLeft = new Paddle("left", 20, 3.5, 25, true, 2, 50, 50, webSocket);
        // const paddleRight = new Paddle("right", 20, 3.5, 25, false, 2, 50, 50, webSocket);
        // const ball = new Ball(50, 50, 0, 1, 10, 1, 19);
        const {ambientLight, light} = createLights();

        loop = new Loop(camera, scene, renderer);
        container.append(renderer.domElement);

        top.position.set(0, 51, 0);
        top.scale.set(50, 1, 1);
        bot.position.set(0, -51, 0);
        bot.scale.set(50, 1, 1);


        // paddleLeft.position.set(-20, 0, 0);
        //paddleRight.position.set(50, 0, 0);
        // paddleLeft.scale.set(1, 5, 1);
        //paddleRight.scale.set(1, 5, 1);

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
        // loop.updatables.push(paddleLeft);
        // loop.updatables.push(ball);
        // loop.updatables.push(cube);

        scene.add(top, bot, light, ambientLight, fontGroup);

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