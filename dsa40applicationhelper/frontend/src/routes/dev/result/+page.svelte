<script lang="ts">
  import ResultViewer from "$lib/ResultViewer.svelte";
  const X1 = {
    question_id: "X1",
    text: "Name, bitte.",
    value: "Joseph Weizenbaum",
  };
  const X2 = {
    question_id: "X2",
    text: "Wohnort, also Land nur in Iso Format",
    value: "DEU",
  };
  const mastodon = { name: "mastodon", answers: [X1, X2] };
  const Z1 = {
    question_id: "Z1",
    text: "Name, bitte.",
    value: "Joseph Weizenbaum",
  };
  const Z2 = {
    question_id: "Z2",
    text: "Hoch geladenes CV",
    value: "Lebenslauf.pdf",
  };
  const myspace = { name: "myspace", answers: [Z1, Z2] };
  const results = [mastodon, myspace];
</script>

<h2>Result View with 2 vlopses</h2>
<ResultViewer {results} />
