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
