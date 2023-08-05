built_modules = list(name for name in
    "Core;Gui;Widgets;PrintSupport;Sql;Network;Test;Concurrent;X11Extras;Xml;XmlPatterns;Help;Multimedia;MultimediaWidgets;OpenGL;OpenGLFunctions;Positioning;Location;Qml;Quick;QuickWidgets;RemoteObjects;Scxml;Script;ScriptTools;Sensors;TextToSpeech;Charts;Svg;DataVisualization;UiTools;WebChannel;WebEngineCore;WebEngine;WebEngineWidgets;WebSockets;3DCore;3DRender;3DInput;3DLogic;3DAnimation;3DExtras"
    .split(";"))

shiboken_library_soversion = str(5.12)
pyside_library_soversion = str(5.12)

version = "5.12.5"
version_info = (5, 12, 5, "", "")

__build_date__ = '2019-09-11T05:37:11+00:00'




__setup_py_package_version__ = '5.12.5'
