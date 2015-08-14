var labelType, useGradients, nativeTextSupport, animate;

(function() {
  var ua = navigator.userAgent,
      iStuff = ua.match(/iPhone/i) || ua.match(/iPad/i),
      typeOfCanvas = typeof HTMLCanvasElement,
      nativeCanvasSupport = (typeOfCanvas == 'object' || typeOfCanvas == 'function'),
      textSupport = nativeCanvasSupport
        && (typeof document.createElement('canvas').getContext('2d').fillText == 'function');
  //I'm setting this based on the fact that ExCanvas provides text support for IE
  //and that as of today iPhone/iPad current text support is lame
  labelType = (!nativeCanvasSupport || (textSupport && !iStuff))? 'Native' : 'HTML';
  nativeTextSupport = labelType == 'Native';
  useGradients = nativeCanvasSupport;
  animate = !(iStuff || !nativeCanvasSupport);
})();

var Log = {
  elem: false,
  write: function(text){
    if (!this.elem)
      this.elem = document.getElementById('log');
    this.elem.innerHTML = text;
    this.elem.style.left = (500 - this.elem.offsetWidth / 2) + 'px';
  }
};


var icicle;

function init(){
  // left panel controls
  controls();
  $jit.id('max-levels').style.display = 'none';
  // init data
  var json = {
    "name": "ESS Linac",
    "id": "linac",
    "children": [
      {
        "name": "High Energy Beam Transport",
        "id": "HEBT",
        "children": [
          {
            "name": "Cell-010",
            "id": "cell010",
            "children": [
                {
                  "name": "Slot-010",
                  "id": "slot010",
                  "children": [
                    {
                      "name": "BLE-010",
                      "id": "ble010",
                      "data": {
                        "$color": "#21ff59"
                      }
                    }
                  ],
                  "data": {
                    "$color": "#59ff21"
                  }
                },
                {
                  "name": "Slot-020",
                  "id": "slot020",
                  "data": {
                    "$color": "#59ff21"
                  }
                }
            ],
            "data": {
              "$color": "#c8ff21"
            }
          }
        ],
        "data": {
          "$color": "#ffc821",
          "description": "This is a section."
        }
      },
      {
        "name": "Accelerator 2 Target",
        "id": "A2T",
        "children": [
          {
            "name": "Cell-010",
            "id": "a2tcell010",
            "children": [
                {
                  "name": "Slot-010",
                  "id": "a2tslot010",
                  "data": {
                    "$color": "#59ff21"
                  }
                },
                {
                  "name": "Slot-020",
                  "id": "a2tslot020",
                  "data": {
                    "$color": "#59ff21"
                  }
                }
            ],
            "data": {
              "$color": "#c8ff21"
            }
          }
        ],
        "data": {
          "$color": "#ffc821",
          "description": "This is another section."
        }
      }
    ],
    "data": {
      "$color": "#ff5921",
      "description": "This is the whole ESS Accelerator.",
      "texto": "A test text."
    }
  };
  // end
  // init Icicle
  icicle = new $jit.Icicle({
    // id of the visualization container
    injectInto: 'infovis',
    // whether to add transition animations
    animate: animate,
    // nodes offset
    offset: 1,
    // whether to add cushion type nodes
    cushion: false,
    // do not show all levels at once
    constrained: true,
    levelsToShow: 4,
    // enable tips
    Tips: {
      enable: true,
      type: 'Native',
      // add positioning offsets
      offsetX: 20,
      offsetY: 20,
      // implement the onShow method to
      // add content to the tooltip when a node
      // is hovered
      onShow: function(tip, node){
        // count children
        var count = 0;
        node.eachSubnode(function(){
          count++;
        });
        // add tooltip info
        tip.innerHTML = "<div class=\"tip-title\"><b>Name:</b> "
            + node.name + "</div>" + "<div class=\"tip-title\"><b>Description:</b> "
                + node.data.description + "</div><div class=\"tip-text\">" + count
            + " children</div>";
      }
    },
    // Add events to nodes
    Events: {
      enable: true,
      onClick: function(node){
        if (node) {
          //hide tips
          icicle.tips.hide();
          // perform the enter animation
          icicle.enter(node);
        }
      },
      onRightClick: function(){
        //hide tips
        icicle.tips.hide();
        // perform the out animation
        icicle.out();
      }
    },
    // Add canvas label styling
    Label: {
      type: labelType, // "Native" or "HTML"
      color: '#333',
      style: 'bold',
      size: 12
    },
    // Add the name of the node in the corresponding label
    // This method is called once, on label creation and only for DOM and
    // not
    // Native labels.
    onCreateLabel: function(domElement, node){
      domElement.innerHTML = node.name;
      var style = domElement.style;
      style.fontSize = '0.9em';
      style.display = '';
      style.cursor = 'pointer';
      style.color = '#333';
      style.overflow = 'hidden';
    },
    // Change some label dom properties.
    // This method is called each time a label is plotted.
    onPlaceLabel: function(domElement, node){
      var style = domElement.style, width = node.getData('width'), height = node
          .getData('height');
      if (width < 7 || height < 7) {
        style.display = 'none';
      } else {
        style.display = '';
        style.width = width + 'px';
        style.height = height + 'px';
      }
    }
  });
  // load data
  icicle.loadJSON(json);
  // compute positions and plot
  icicle.layout.orientation = 'v';
  icicle.refresh();
  //end
}

//init controls
function controls() {
  var jit = $jit;
  var gotoparent = jit.id('update');
  jit.util.addEvent(gotoparent, 'click', function() {
    icicle.out();
  });
  var select = jit.id('s-orientation');
  jit.util.addEvent(select, 'change', function () {
    icicle.layout.orientation = select[select.selectedIndex].value;
    icicle.refresh();
  });
  var levelsToShowSelect = jit.id('i-levels-to-show');
  jit.util.addEvent(levelsToShowSelect, 'change', function () {
    var index = levelsToShowSelect.selectedIndex;
    if(index == 0) {
      icicle.config.constrained = false;
    } else {
      icicle.config.constrained = true;
      icicle.config.levelsToShow = index;
    }
    icicle.refresh();
  });
}
//end
