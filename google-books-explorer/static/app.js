let Books = {
  data() {
    return {
      q: '',
      currentPage: 0,
      books: [],
      loading: false,
    }
  },
  delimiters: ['[[', ']]'],
  mounted() {
    console.log('bonjour');
    window.onscroll = () => {
      if (window.scrollY + window.innerHeight >= document.body.offsetHeight - 1000) {
        this.currentPage += 1;
        this.fetchMoreBooks();
      }
    }
  },
  methods: {
    async fetchBooks(e) {
      e.preventDefault();
      this.loading = true;
      this.books = new Array(15);
      let q = this.q.replace(/\s+/g, ' ').trim();
      let response = await fetch(`/search/?q=${encodeURI(q)}`);
      let books = await response.json();
      this.books = books;
      this.loading = false;
    },

    async fetchMoreBooks() {
      this.loading = true;
      let q = this.q.replace(/\s+/g, ' ').trim();
      let response = await fetch(`/search/?q=${encodeURI(q)}&page=${encodeURI(this.currentPage)}`);
      let moreBooks = await response.json();
      console.log(moreBooks)
      if (moreBooks.length) {
        this.books.push(...moreBooks);
        console.log(this.books.length);
      } else {
        console.log('No more books');
        this.loading = false;
        return;  // why
      }
      this.loading = false;
    },
  }
}

Vue.createApp(Books).mount('#app')

// more todos
