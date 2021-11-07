const app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    q: '',
    books: [],
    loading: false,
  },
  methods: {
    async fetchBooks(e) {
      e.preventDefault();
      this.loading = true;
      this.books = new Array(20);
      let q = this.q.replace(/\s+/g, " ").trim();
      let response = await fetch(`/search/?q=${encodeURI(q)}`);
      let books = await response.json();
      this.books = books;
      this.loading = false;
    }
  },
})