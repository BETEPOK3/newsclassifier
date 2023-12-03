 let multiselect_block = document.querySelectorAll(".multiselect_block");
    multiselect_block.forEach(parent => {
        let label = parent.querySelector(".field_multiselect");
        let select = parent.querySelector(".field_select");
        let text = label.innerHTML;

         let selectedOptions = select.selectedOptions;
            label.innerHTML = "";
            for (let option of selectedOptions) {
                let button = document.createElement("button");
                button.type = "button";
                button.className = "btn_multiselect";
                button.textContent = option.textContent;
                button.onclick = _ => {
                    option.selected = false;
                    button.remove();
                    if (!select.selectedOptions.length){
                         for(let op of select.options){
                               if(op.value == "all"){
                                   op.selected = true;
                                   button.textContent = op.textContent;
                                   label.append(button);
                               }
                         }
                    }
                };
                label.append(button);
            }

        select.addEventListener("change", function(element) {
            label.innerHTML = "";
            if(select.selectedOptions.length === 0){
               for(let op of select.options){
                   if(op.value == "all"){
                        let button = document.createElement("button");
                        button.type = "button";
                        button.className = "btn_multiselect";
                        button.textContent =  option.textContent;
                       button.onclick = _ => {
                            op.selected = false;
                            button.remove();
                            if (!select.selectedOptions.length){
                                 for(let op of select.options){
                                       if(op.value == "all"){
                                           op.selected = true;
                                           button.textContent = op.textContent;
                                           label.append(button);
                                       }
                                 }
                            }
                        };
                        label.append(button);
                   }
               }
            }
            for (let i=0; i<select.selectedOptions.length; i++) {
                let option = select.selectedOptions[i];
               if(!(option.value == "all" && select.selectedOptions.length > 1)){
                        let button = document.createElement("button");
                        button.type = "button";
                        button.className = "btn_multiselect";
                        button.textContent =  option.textContent;
                        button.onclick = _ => {
                            option.selected = false;
                            for(let op of select.options){
                                       if(op.value == "all"){
                                           op.selected = false;
                                       }
                                 }
                            button.remove();
                            if (!select.selectedOptions.length){
                                 for(let op of select.options){
                                       if(op.value == "all"){
                                           op.selected = true;
                                           button.textContent = op.textContent;
                                           label.append(button);
                                       }
                                 }
                            }
                        };
                        label.append(button);
                }
               else {
                   option.selected = false;
                   i--;
               }
            }
        })
    })