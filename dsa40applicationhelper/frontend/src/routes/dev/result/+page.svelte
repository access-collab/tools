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
  const X3 = {
    question_id: "X3",
    text: "ein Tagebucheintrag",
    value: `Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin cursus tincidunt dui. Suspendisse eu sollicitudin enim. In vel augue convallis, varius est eget, tempor odio. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Integer a lectus ex. Cras finibus placerat porta. Mauris sem diam, viverra quis odio vel, sagittis dapibus ex. Mauris gravida ullamcorper elementum. Praesent ullamcorper ex ut arcu faucibus, sed ultricies turpis sollicitudin. Duis rhoncus odio sit amet dolor porta fermentum. Donec a velit dolor. Donec bibendum in purus sed pretium. Nulla at purus libero.

Aenean porta pellentesque ligula. Vivamus pretium iaculis tellus sed dictum. Aenean imperdiet enim nisl. Vivamus et mauris id nulla posuere gravida. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nam turpis nunc, tempor ut lacus ut, tincidunt lobortis neque. Cras commodo dolor turpis, non laoreet augue convallis eu. Curabitur finibus sed ligula id scelerisque. Fusce interdum augue in turpis fringilla sollicitudin. Proin maximus tincidunt quam eu rhoncus. Aenean eleifend lectus sed metus efficitur, ac convallis quam rhoncus. Quisque vehicula ligula ut dui lobortis, non ultrices nulla tincidunt. Sed sit amet dignissim ex.

Aliquam felis nisl, accumsan ac dui sit amet, interdum bibendum sapien. Curabitur volutpat vestibulum placerat. Vivamus rutrum, quam a lacinia tincidunt, orci eros placerat magna, non hendrerit lorem tortor et purus. Morbi at risus eu metus sollicitudin ultricies. Maecenas porttitor nunc nec nibh eleifend auctor. Aenean tristique, nibh vel cursus commodo, magna justo sollicitudin mi, sit amet vestibulum nisl orci nec mi. Quisque malesuada elit lectus, at ultrices nisl scelerisque suscipit. Aenean imperdiet magna sed felis accumsan condimentum. Vivamus pellentesque feugiat risus, sit amet ultrices ante. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Cras sit amet erat eu felis facilisis blandit eget in lorem. Aliquam erat volutpat.

Curabitur vel nulla neque. Integer ipsum diam, feugiat ut euismod sit amet, maximus ac velit. Quisque tincidunt arcu in ante suscipit, sed blandit tellus dictum. Donec fermentum mauris vitae pretium laoreet. Pellentesque nec nulla turpis. Duis in odio vitae purus iaculis pellentesque. Ut pharetra scelerisque leo, ut condimentum dolor lobortis pretium.

Sed sodales augue ultrices tempor molestie. Aenean tortor nisl, pretium eu eros sit amet, pretium rhoncus odio. Etiam quam mauris, molestie ac lectus et, mollis elementum lacus. Nulla consequat lectus fringilla massa rutrum, a efficitur velit fermentum. Quisque viverra dolor in auctor varius. Sed vel massa non lorem consequat dapibus. Duis sed consequat nulla, ac venenatis orci. Donec a lectus mi. Nullam id bibendum nisl. Etiam sed lectus sit amet metus convallis cursus.`,
  };
  const mastodon = { name: "mastodon", answers: [X1, X2, X3] };
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
