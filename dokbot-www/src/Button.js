
function Button({ isLoading, children, ...props }) {
  return (
    <button className="button" {...props}>
      {isLoading && (<span>Loading...</span>)}
      {!isLoading && children}
    </button>
  );
}

export default Button