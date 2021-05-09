<template>
  <div class="">
    <span class="font-extrabold height: 100% width:25% float:left"
      >Fecha por Pagar:
    </span>
    <span>{{ bill.issuedate }}</span>
    <br />
    <span class="font-extrabold height: 100% width:25% float:left"
      >Fecha de Pago:
    </span>
    <span>{{ bill.paymentday }}</span>
    <br />
    <span class="font-extrabold height: 100% width:25% float:left"
      >Cliente:
    </span>
    <span>{{ bill.clientname }}</span>
    <br />
    <span class="font-extrabold height: 100% width:25% float:left"
      >Costo:
    </span>
    <span>{{ bill.cost }}</span>
    <br />
    <span class="font-extrabold height: 100% width:25% float:left"
      >Método de Pago:
    </span>
    <span>{{ bill.paymethod.name }}</span>
    <br />
  </div>
</template>
<script>

export default {
    name:'BillInfo',
    props:{
        bill:{}
    }
};
</script>