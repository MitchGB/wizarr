<template>
    <div>
        <!-- Form -->
        <FormKit type="form" id="serverForm" v-model="serverForm" class="space-y-4 md:space-y-6" :actions="false" @submit="saveConnection">
            <!-- Server Name -->
            <FormKit type="text" :label="__('SMTP Address')" :help="__('Address of your SMTP server')" name="smtp_address" placeholder="smtp.domain.com" validation="required" required autocomplete="text" />

            <FormKit type="number" :label="__('SMTP Port')" :help="__('Port of your SMTP server')" name="smtp_port" validation="required" required />

            <FormKit type="text" :label="__('SMTP Username')" :help="__('Authentication Username')" name="smtp_username" placeholder="username" validation="required" required autocomplete="text" />

            <FormKit type="password" :label="__('SMTP Password')" :help="__('Authentication Password')" name="smtp_password" validation="required" required />

        </FormKit>

        <!-- Buttons -->
        <div class="flex flex-col sm:flex-row">
            <div class="flex flex-grow justify-end sm:justify-end space-x-2 mt-2">
                <!-- Save  -->
                <FormKit type="button" v-if="!saved" @click="$formkit.submit('serverForm')">
                    {{ __("Save") }}
                </FormKit>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { Collapse } from "vue-collapsed";

import ScanLibraries from "../ScanLibraries/ScanLibraries.vue";
import ScanServers from "../ScanServers/ScanServers.vue";

export default defineComponent({
    name: "ServerSettings",
    components: {
        Collapse,
    },
    props: {
        setup: {
            type: Boolean,
            default: false,
        },
    },
    data() {
        return {
            verified: false,
            saved: false,
            serverForm: {
                smtp_address: "",
                smtp_username: "",
                smtp_password: "",
                smtp_port: 0,
            }
        };
    },
    methods: {
        syncSettings() {
            this.$axios.get("/api/settings", { disableErrorToast: true }).then((response) => {
                if (response.data)
                    console.log(response.data)
                    this.serverForm = {
                        ...this.serverForm,
                        ...response.data,
                    };
            });
        },
        async saveConnection() {
            const formData = new FormData();

            formData.append("smtp_address", this.serverForm.smtp_address);
            formData.append("smtp_username", this.serverForm.smtp_username);
            formData.append("smtp_password", this.serverForm.smtp_password);
            formData.append("smtp_port", this.serverForm.smtp_port);

            console.log(formData)

            const response = await this.$axios.put("/api/settings", formData).catch(() => {
                this.$toast.error(this.__("Unable to save settings."));
            });

            if (!response?.data) return;

            this.saved = true;
            this.$toast.info("SMTP settings saved successfully!");
        },
    },
    mounted() {
        this.syncSettings();
    },
});
</script>
