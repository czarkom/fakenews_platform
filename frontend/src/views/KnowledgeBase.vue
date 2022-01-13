<template>
  <div>
    <div class="text-xl text-gray-800 font-bold m-4 text-left">
      Baza wiedzy
    </div>
    <div class="flex justify-center text-2xl font-semibold">
      Autorzy
    </div>
    <div class="flex w-full justify-center my-4">
      <div class="w-1/4"></div>
      <div class="w-1/4 flex flex-col items-center">
        <div>
          <img :src="require('@/assets/resources/ja.jpg')" class="h-32 rounded-full">
        </div>
        <div class="font-semibold">
          Maciej
        </div>
      </div>
      <div class="w-1/4 flex flex-col items-center">
        <div>
          <img :src="require('@/assets/resources/misz.jpg')" class="h-32 rounded-full">
        </div>
        <div class="font-semibold">
          Miłosz
        </div>
      </div>
      <div class="w-1/4"></div>
    </div>
    <div class="flex">
      <div class="w-1/6"></div>
      <div class="w-2/3 my-4 text-center font-semibold flex">
        <div class="w-1/6 flex font-bold text-5xl text-gray-500 items-end justify-end">
          ,,
        </div>
        <div class="w-2/3 m-2">
          Nazywamy się Maciej Czarkowski i Miłosz Wójcik. Jesteśmy studentami Politechniki Warszawskiej oraz pasjonatami
          inżynierii danych oraz
          oprogramowania.
          Razem z dr inż. Krzysztofem Hryniówem postanowiliśmy zwalczyć powszechnie panującą dezinformację.
          Stworzona przez nas platforma pozwala na segregację informacji znajdowanych w Internecie na te warte uwagi
          oraz te warte szczególnej weryfikacji. Rozwiązanie to ma pozwolić na bardziej świadome korzystanie z
          internetu,
          pozwalające na odfiltrowywanie artykułów dalece stronniczych lub stworzonych jako <span class="italic">clickbaity</span>,
          które mają jedynie przyciągnąć użytkownika.
        </div>
        <div class="w-1/6 flex font-bold text-5xl text-gray-500">
          <span>&#8243;</span>
        </div>
      </div>
      <div class="w-1/6"></div>
    </div>
    <div class="my-2 flex justify-center text-2xl font-semibold">
      Wykorzystane technologie
    </div>
    <swiper
        :modules="modules"
        :slides-per-view="3"
        :space-between="50"
        :navigation="true"
        :autoplay="true"
        :pagination="{ clickable: true }"
        @swiper="onSwiper"
        @slideChange="onSlideChange"
    >
      <swiper-slide>
        <div class="h-40 flex justify-center items-center my-4">
          <img class="h-24" :src="require('@/assets/resources/logos/vue.jpg')">
        </div>
      </swiper-slide>
      <swiper-slide>
        <div class="h-40 flex justify-center items-center my-4">
          <img class="h-24" :src="require('@/assets/resources/logos/tensorflow.jpg')">
        </div>
      </swiper-slide>
      <swiper-slide>
        <div class="h-40 flex justify-center items-center my-4">
          <img class="h-32" :src="require('@/assets/resources/logos/requests-html-logo-new.jpg')">
        </div>
      </swiper-slide>
      <swiper-slide>
        <div class="h-40 flex justify-center items-center my-4">
          <img class="h-32" :src="require('@/assets/resources/logos/bs.jpg')">
        </div>
      </swiper-slide>
      <swiper-slide>
        <div class="h-40 flex justify-center items-center my-4">
          <img class="h-32" :src="require('@/assets/resources/logos/pandas.jpg')">
        </div>
      </swiper-slide>
      <swiper-slide>
        <div class="h-40 flex justify-center items-center my-4">
          <img class="h-32" :src="require('@/assets/resources/logos/matplotlib.jpg')">
        </div>
      </swiper-slide>
      <swiper-slide>
        <div class="h-40 flex justify-center items-center my-4">
          <img class="h-24" :src="require('@/assets/resources/logos/flask.jpg')">
        </div>
      </swiper-slide>
      <swiper-slide>
        <div class="h-40 flex justify-center items-center my-4">
          <img class="h-32" :src="require('@/assets/resources/logos/mysql.jpg')">
        </div>
      </swiper-slide>
      <swiper-slide>
        <div class="h-40 flex justify-center items-center my-4">
          <img class="h-32" :src="require('@/assets/resources/logos/docker.jpg')">
        </div>
      </swiper-slide>
      ...
    </swiper>
    <div class="my-8">
      <div class="my-4 flex justify-center text-2xl font-semibold">
        Analiza stron internetowych
      </div>
      <div class="flex w-full justify-center">
        <div class="w-1/6"></div>
        <div class="w-2/3 mb-4">
          <p class="text-justify">
            Podstawą uczenia modelu sieci neuronowej oraz predykcji wiarygodności strony jest zdobycie danych, które
            mogą
            zasilić model. W tym celu konieczne było wykorzystanie webscrappingu, czyli procesu pozyskiwania informacji
            o
            danej witrynie poprzez analizę jej kodu. Wywołanie w naszej aplikacji analizy podanego źródła inicjuje
            proces,
            który rozpoczyna się tego typu analizą. Co istotne, strona jest renderowana na serwerze aplikacji, aby
            zapewnić możliwość analizy składniowej treści wygenerowanej przez skrypty języka JavaScript, który
            dynamicznie
            tworzy stronę już po pobraniu jej kodu z serwera. Krótkie wyjaśnienie czym jest webscrapping, prezentuje
            poniższe wideo autorstwa kanału <a class="text-blue-700"
                                               href="https://www.youtube.com/channel/UCRfbcJQu9HZvc7uks2wmGzw">ParseHub</a>
            w serwisie YouTube.
          </p>
        </div>
        <div class="w-1/6"></div>

      </div>
      <div class="w-full text-center">
        <iframe width="560" height="315" src="https://www.youtube.com/embed/Ct8Gxo8StBU" title="YouTube video player"
                frameborder="0" class="inline-block"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen></iframe>
      </div>
    </div>
    <div class="my-8">
      <div class="my-4 flex justify-center text-2xl font-semibold">
        Sieć neuronowa
      </div>
      <div class="flex w-full justify-center">
        <div class="w-1/6"></div>
        <div class="w-2/3 mb-4">
          <p class="text-justify">
            Pozyskane w procesie webscrappingu dane zostały poddane analizie statystycznej oraz przekazane do treningu
            sieci neuronowej. W celu uzyskania największej skuteczności poprawnych klasyfikacji stron oraz nie
            spowodowania przy tym zbytniego dopasowania się do danych uczących, postanowiliśmy skorzystać ze zbioru
            walidacyjnego i walidacji krzyżowej. Wielorakie analizy skłoniły nas do dokonania modyfikacji w zakresie
            przetwarzanych cech. Na podstawie macierzy korelacji odrzuciliśmy niektóre cechy o wysokim współczynniku
            oraz stworzyliśmy nowe cechy, które zwiększyły różnorodność danych uczących i dały szanse do poprawy
            uczonemu modelowi sieci neuronowej. Wybrany przez nas model implementuje technologię LSTM (Long-short term
            memory), która, dzięki zapamiętywaniu stanów i stosowaniu mechanizmu sprzężenia zwrotnego, pozwala na
            sprawniejsze uzyskiwanie skuteczniejszych klasyfikacji. Schemat komórki tego typu sieci neuronowej
            prezentuje poniższa infografika.
          </p>
          <div class="flex justify-center my-4">
            <img class="h-72" src="@/assets/resources/lstm_architecture.jpg">
          </div>
        </div>
        <div class="w-1/6"></div>
      </div>
    </div>
    <div class="my-8">
      <div class="my-4 flex justify-center text-2xl font-semibold">
        Szczegółowe sprawozdanie z projektu (praca dyplomowa inżynierska)
      </div>
      <div class="w-full justify-center flex font-semibold">
        <div class="flex justify-center">
          <a href="/Fakenews_platform_Czarkowski_Wojcik.pdf" download class="text-center hover:text-blue-700">
            <img src="@/assets/resources/pdf_icon.jpg" class="h-20">
            <span class="text-center">Pobierz</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SwiperCore, {Pagination, Navigation, Scrollbar, A11y, Autoplay} from 'swiper';
import {Swiper, SwiperSlide} from 'swiper/vue';
import 'swiper/swiper.scss';
import 'swiper/components/pagination/pagination.scss'
import 'swiper/components/navigation/navigation.scss'
import axios from "axios";

export default {
  name: "KnowledgeBase",
  components: {
    Swiper,
    SwiperSlide
  },
  beforeCreate() {
    SwiperCore.use([Pagination, Navigation, Autoplay]);
  },
  setup() {
    const onSwiper = (swiper) => {
      console.log(swiper);
    };
    const onSlideChange = () => {
      console.log('slide change');
    };
    return {
      onSwiper,
      onSlideChange,
      modules: [Navigation, Pagination, Scrollbar, A11y, Autoplay],
    };
  },
  methods: {}
}
</script>

<style scoped>

</style>