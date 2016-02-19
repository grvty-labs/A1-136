var PropTypes = React.PropTypes;

var Square = React.createClass({
  propTypes: {
    black: PropTypes.bool
  },

  render: function () {
    var internal_color = this.props.black;
    var fill = internal_color ? 'black' : 'white';
    var stroke = internal_color ? 'white' : 'black';

    return (
      <div style={{ backgroundColor: fill,
          color: stroke,
          width: '100%',
          height: '100%' }}>
        {this.props.children}
      </div>
    );
  }
});

//module.exports = Square;
