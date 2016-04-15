var React = require('react');
var PropTypes = React.PropTypes;
var Isometric = require('./isometric');
var ReactCSSTransitionGroup = require('react-addons-css-transition-group');

var Cluster = React.createClass({
  getInitialState() {
      return {
          selected: 'not-selected',
      };
  },

  propTypes: {
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
    isometric_images: PropTypes.array.isRequired,
    firstImage: PropTypes.string.isRequired,
  },

  changeState: function() {
    this.setState({selected: this.state.selected === 'selected' ? 'not-selected' : 'selected' });
  },
  toggleHidden: function() {
    if(this.state.selected=='not-selected'){
      category = document.getElementById("category-selector").value;
      imagesToFade = document.getElementById(category).getElementsByClassName("cluster-images");
      for(i = 0 ; i< imagesToFade.length ; i++){
        imagesToFade[i].className = "cluster-images not-selected inactive";
      }
    }
    else{
      imagesToFade = document.getElementsByClassName("cluster-images not-selected inactive");
      longitud = imagesToFade.length;
      for(i = 0 ; i< longitud ; i++){
        //this is 0 because the array is getting smaller dinamically, so we change the first image always
        imagesToFade[0].className = "cluster-images not-selected";
      } 
    }
    this.changeState();
  },
  render: function () {
    if (this.state == undefined){
      return (
        <div>Loading</div>
        )
    }
    else{
      var hiddenIsos = false;
      var isoNumber = 0;
      selected = this.state.selected;
      imageLocation = this.props.firstImage;
      var IsometricNodes = this.props.isometric_images.map(function (isoimage) {
        loc = imageLocation;
        imageLocation = (imageLocation=='left') ? 'right':'left';
        var number = isoNumber;
        isoNumber ++;
        var hideMe = hiddenIsos;
        if(selected == 'not-selected'){
          hiddenIsos = true;
          selectMe = false;
        }
        else
          selectMe = true;
        return (
            <Isometric 
              hide = {hideMe}
              listNumber = {number}
              selected = {selectMe}
              imageUrl={isoimage.url}
              key={isoimage.id}
              imageId={isoimage.id}
              imageLoc={loc}
            />
        );
      });
      className = "cluster-images " + this.state.selected;
      return (
        <div key={this.props.id} onClick={this.toggleHidden} className={className}>
            {IsometricNodes}
        </div>
      );
    }
  },

});

module.exports = Cluster;
