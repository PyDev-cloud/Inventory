class SubCategoryAndFileUploadView(FormView):
    # This view will handle both SubCategory form submission and file uploads
    template_name = 'subcategory/Subcategorycreate.html'
    # We use both forms (manual form and file upload form)
    form_class = SubCategoryForm  # Default form for manual SubCategory creation
    file_form_class = FileUploadForm  # Form for file uploads
    
    # Success URL for file upload or form submission
    success_url = '/subcategoryList/'

    def get(self, request, *args, **kwargs):
        """
        Handles GET request. Renders both the file upload form and the manual SubCategory form.
        """
        file_form = FileUploadForm()
        subcategory_form = SubCategoryForm()
        return render(request, self.template_name, {
            'file_form': file_form,
            'subcategory_form': subcategory_form,
        })

    def post(self, request, *args, **kwargs):
        """
        Handles POST request for either file upload or manual SubCategory creation.
        It checks which form was submitted and processes it accordingly.
        """
        file_form = FileUploadForm(request.POST, request.FILES)
        subcategory_form = SubCategoryForm(request.POST)

        # If the file form was submitted
        if 'file' in request.FILES:
            if file_form.is_valid():
                uploaded_file = request.FILES['file']
                if uploaded_file.name.endswith('.csv'):
                    # Process CSV file
                    self.upload_csv(uploaded_file)
                    messages.success(request, "CSV file processed successfully!")
                elif uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
                    # Process Excel file
                    self.upload_excel(uploaded_file)
                    messages.success(request, "Excel file processed successfully!")
                else:
                    messages.error(request, "Invalid file type. Only CSV and Excel files are allowed.")
                return redirect('subcategory_list')  # Redirect after successful file processing
        elif subcategory_form.is_valid():
            # If the manual SubCategory form was submitted
            category_name = subcategory_form.cleaned_data['category']
            subcategory_name = subcategory_form.cleaned_data['name']
            category, created_category = Category.objects.get_or_create(name=category_name)
            
            if created_category:
                messages.success(request, f"Category '{category_name}' created.")
            else:
                messages.info(request, f"Category '{category_name}' already exists.")
            
            SubCategory.objects.create(name=subcategory_name, category=category)
            messages.success(request, f"SubCategory '{subcategory_name}' created successfully!")
            return redirect('subcategory_list')  # Redirect after successful form submission

        # If neither form is valid, render the page with error messages
        return render(request, self.template_name, {
            'file_form': file_form,
            'subcategory_form': subcategory_form,
        })

    def form_invalid(self, form):
        # Handle invalid form submissions
        #messages.error(self.request, "Please correct the errors below.")  # Error message
        return super().form_invalid(form)

    def upload_csv(self, file):
        # Read the CSV file
        df = pd.read_csv(file)

        print("CSV Columns:", df.columns)  # Debugging step

        # Iterate over the rows and create Category and SubCategory
        for index, row in df.iterrows():
            category_name = row.get('category', None)
            subcategory_name = row.get('subcategory', None)

            if not category_name or not subcategory_name:
                print(f"Row {index} is missing category or subcategory, skipping.")
                continue

            # Ensure category exists or create it
            category, created_category = Category.objects.get_or_create(name=category_name)
            if created_category:
                print(f"Category '{category_name}' created.")
            else:
                print(f"Category '{category_name}' already exists.")

            # Create SubCategory and link it to the Category
            subcategory, created_subcategory = SubCategory.objects.get_or_create(name=subcategory_name, category=category)
            if created_subcategory:
                print(f"SubCategory '{subcategory_name}' created and linked to '{category_name}'.")
            else:
                print(f"SubCategory '{subcategory_name}' already exists for '{category_name}'.")

        print(f"Finished processing {len(df)} rows.")

    def upload_excel(self, file):
        # Read the Excel file
        df = pd.read_excel(file)

        print("Excel Columns:", df.columns)  # Debugging step

        # Iterate over the rows and create Category and SubCategory
        for index, row in df.iterrows():
            category_name = row.get('category', None)
            subcategory_name = row.get('subcategory', None)

            if not category_name or not subcategory_name:
                print(f"Row {index} is missing category or subcategory, skipping.")
                continue

            # Ensure category exists or create it
            category, created_category = Category.objects.get_or_create(name=category_name)
            if created_category:
                print(f"Category '{category_name}' created.")
            else:
                print(f"Category '{category_name}' already exists.")

            # Create SubCategory and link it to the Category
            subcategory, created_subcategory = SubCategory.objects.get_or_create(name=subcategory_name, category=category)
            if created_subcategory:
                print(f"SubCategory '{subcategory_name}' created and linked to '{category_name}'.")
            else:
                print(f"SubCategory '{subcategory_name}' already exists for '{category_name}'.")

        print(f"Finished processing {len(df)} rows.")