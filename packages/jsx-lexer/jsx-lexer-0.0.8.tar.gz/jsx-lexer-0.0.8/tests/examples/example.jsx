const isOldEnough = (value, ownProps) => {
    if (parseInt(value, 10) < 14) {
        return "Only 14yo and older can register to the site."
    }
};

// functional component
const BlogTitle = ({ children }) => (
  <h3>{children}</h3>
);

// class component
class BlogPost extends React.Component {
  renderTitle(title) {
    return <BlogTitle>{title}</BlogTitle>
  };
  render() {
    return (
    <div className="blog-body">
      {this.renderTitle(this.props.title)}
      <p>{this.props.body}</p>
      <input type="text" {...props.inputProps} />
    </div>
    );
  }
}

const body = "Hello World!";
const blogNode = <BlogPost title="What's going on?" body={body} />;
// some comment. Tags shouldn't be lexed in here
// <div class="blog-body">
// <h3>What's going on?</h3>
// <p>Hello World!</p>
// </div>

/*
  Some comment. Tags shouldn't be lexed in here either
  <div class="blog-body">
  <h3>What's going on?</h3>
  <p>Hello World!</p>
  </div>
*/

function Pagination(props, children) {
   var list = [];
   var _class;
   for (var i=0; i<props.size; i++) {
      if (i == props.selected) {
        _class = 'selected';
      } else {
        _class = '';
      }
      list.push(<li class={_class}>{i}</li>);
   }
   return (<ul>{list}</ul>);
}
