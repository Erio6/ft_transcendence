import {TextGeometry} from 'three/addons/geometries/TextGeometry.js';
import {FontLoader} from "three/addons/loaders/FontLoader.js";
import {MeshStandardMaterial} from "three";
import {Mesh} from "three";

let font;

const Align = {
    Left: 0,
    Center: 1,
    Right: 2,
}

function loadFont(scene, x, y, z, score, group = null, existingMesh = null, align = Align.Center, size = 10) {
    const loader = new FontLoader();
    loader.load(
        '/static/js/threejs/Components/fonts/helvetiker_regular.typeface.json',
        function (fontParam) {
            font = fontParam;
            generateObject(scene, x, y, z, score, group, existingMesh, align, size);
        });
}

function generateObject(scene, x, y, z, score, group = null, existingMesh = null, align = Align.Center, size = 10) {
    // console.log(font);
    const geometry = new TextGeometry(score, {
        font: font,
        size: size,
        depth: 1,
        curveSegments: 12,
        bevelEnabled: false,
        bevelThickness: 0.1,
        bevelSize: 0,
        bevelOffset: 0,
        bevelSegments: 5
    });
    geometry.computeBoundingBox();
    let offsetX, offsetY;
    switch (align) {
        case Align.Left:
            offsetX = 0;
            offsetY = 0;
            break;
        case Align.Center:
            offsetX = geometry.boundingBox.max.x / 2;
            offsetY = geometry.boundingBox.max.y / 2;
            break;
        case Align.Right:
            offsetX = geometry.boundingBox.max.x;
            offsetY = 0;
            break;
        default:
            break;
    }

    if (existingMesh) {
        existingMesh.geometry.dispose();
        existingMesh.geometry = geometry;
        existingMesh.position.set(-offsetX + x, -offsetY + y, z);
    } else {
        const material = new MeshStandardMaterial({color: 0x422e0f});
        const materials = [material, material];
        const model = new Mesh(geometry, materials);
        // console.log(model + " | " + x + " | " + y + " | " + z);
        model.receiveShadow = true;
        model.position.set(-offsetX + x, -offsetY + y, z);
        if (group)
            group.add(model);
        else
            scene.add(model);
        return model;
    }
}

function createFont(scene, x = 0, y = 0, z = -5, score = "00", group = null, existingMesh = null, align = Align.Center, size = 10) {
    loadFont(scene, x, y, z, score, group, existingMesh, align, size); // Wait for the font to load

}

export {createFont, Align};