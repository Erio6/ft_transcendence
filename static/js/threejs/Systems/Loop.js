import {Clock} from "three";

const clock = new Clock();

class Loop {
    constructor(camera, scene, renderer) {
        this.camera = camera;
        this.scene = scene;
        this.renderer = renderer;
        this.pause = false;
        this.updatables = [];

        addEventListener("keydown", (event) => {
            if (event.code === "Space")
                this.pause = !this.pause;
        });
    }

    start() {
        this.renderer.setAnimationLoop(() => {
            this.tick();
            this.renderer.render(this.scene, this.camera);
        })
    }

    stop() {
        this.renderer.setAnimationLoop(null);
    }

    tick() {
        if (this.pause === true)
            return;
        const delta = clock.getDelta();
        for (const object of this.updatables) {
            object.tick(delta);
        }
    }
}

export {Loop};