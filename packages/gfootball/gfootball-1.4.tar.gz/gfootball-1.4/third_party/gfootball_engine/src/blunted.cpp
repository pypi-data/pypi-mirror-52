// Copyright 2019 Google LLC & Bastiaan Konings
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// written by bastiaan konings schuiling 2008 - 2014
// this work is public domain. the code is undocumented, scruffy, untested, and should generally not be used for anything important.
// i do not offer support, so don't ask. to be used for inspiration :)

#include "blunted.hpp"

#include "base/log.hpp"
#include "base/properties.hpp"
#include "base/utils.hpp"
#include "framework/scheduler.hpp"
#include "loaders/aseloader.hpp"
#include "loaders/imageloader.hpp"
#include "main.hpp"
#include "managers/environmentmanager.hpp"
#include "managers/resourcemanager.hpp"
#include "managers/scenemanager.hpp"
#include "managers/systemmanager.hpp"
#include "scene/objectfactory.hpp"
#include "scene/objects/camera.hpp"
#include "scene/objects/geometry.hpp"
#include "scene/objects/image2d.hpp"
#include "scene/objects/joint.hpp"
#include "scene/objects/light.hpp"
#include "scene/objects/skybox.hpp"
#include "scene/resources/geometrydata.hpp"
#include "scene/resources/surface.hpp"
#include "systems/isystem.hpp"
#include "wrap_SDL_ttf.h"

namespace blunted {

  void RegisterObjectTypes(ObjectFactory* objectFactory);

  void Initialize(Properties &config) {
    // initialize resource managers
    GetContext().geometry_manager.RegisterLoader("ase",
                                                 &GetContext().aseLoader);
    GetContext().surface_manager.RegisterLoader("jpg",
                                                &GetContext().imageLoader);
    GetContext().surface_manager.RegisterLoader("png",
                                                &GetContext().imageLoader);
    GetContext().surface_manager.RegisterLoader("bmp",
                                                &GetContext().imageLoader);
    TTF_Init();
    RegisterObjectTypes(&GetContext().object_factory);
  }

  void DoStep() { GetContext().scheduler.Run(); }

  Scheduler *GetScheduler() { return &GetContext().scheduler; }

  void Exit() {
    GetContext().scene_manager.Exit();
    GetContext().object_factory.Exit();
    GetContext().system_manager.Exit();
    TTF_Quit();
    SDL_Quit();
  }


  // additional functions

  void RegisterObjectTypes(ObjectFactory *objectFactory) {
    boost::intrusive_ptr<Camera> camera(new Camera("Camera prototype"));
    objectFactory->RegisterPrototype(e_ObjectType_Camera, camera);
    boost::intrusive_ptr<Image2D> image2D(new Image2D("Image2D prototype"));
    objectFactory->RegisterPrototype(e_ObjectType_Image2D, image2D);
    boost::intrusive_ptr<Geometry> geometry(new Geometry("Geometry prototype"));
    objectFactory->RegisterPrototype(e_ObjectType_Geometry, geometry);
    boost::intrusive_ptr<Skybox> skybox(new Skybox("Skybox prototype"));
    objectFactory->RegisterPrototype(e_ObjectType_Skybox, skybox);
    boost::intrusive_ptr<Light> light(new Light("Light prototype"));
    objectFactory->RegisterPrototype(e_ObjectType_Light, light);
    boost::intrusive_ptr<Joint> joint(new Joint("Joint prototype"));
    objectFactory->RegisterPrototype(e_ObjectType_Joint, joint);
  }

}
