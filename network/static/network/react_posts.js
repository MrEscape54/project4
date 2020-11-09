class Posts extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            posts: []
        };
    }
    
    componentDidMount() {
        fetch("/posts")
          .then(response => response.json())
          .then(items => {
                    this.setState({
                        isLoaded: true,
                        posts: items
                    });
            },
            (error) => {
              this.setState({
                isLoaded: true,
                error
              });
            }
          )
      }

    render() {
        const { error, isLoaded, posts } = this.state;

        if (error) {
          return <div>Error: {error.message}</div>;
        } else if (!isLoaded) {
          return <div>Loading...</div>;
        } else {
            console.log(error);
            console.log(isLoaded);
            console.log(posts);
          return (
            <div > {
                posts.map((post, i) => {
                return (
                    <div className="ui raised very padded text container segment" key={i}>
                        < div className="ui feed">
                            <div className="event">
                                    <div className="label"><img src={post.author.avatar}/></div>
                                <div className="content">
                                    <div className="summary">
                                        <a href={post.author.profile}>{post.author.user} </a>
                                        {post.author.name}
                                        <div className="date">
                                        {post.created}
                                        </div>
                                    </div>
                                    <div className="extra text">
                                        {post.message}
                                    </div>
                                    <div className="meta">
                                        <a className="like">
                                        <i className="like icon"></i> {post.likes} Likes
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    )
                })
            }
            </div>       
          )
        }
        
    }
}

ReactDOM.render(<Posts />, document.querySelector("#posts"));
