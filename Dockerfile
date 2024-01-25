# Use a Raspberry Pi compatible base image
FROM balenalib/raspberry-pi-python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Copy entrypoint script into the container
COPY entrypoint.sh ./
RUN chmod +x /usr/src/app/entrypoint.sh

# Start the application via the entrypoint script
ENTRYPOINT ["./entrypoint.sh"]
CMD ["python", "./app.py"]

# Commands:
# docker build -t power-app .
# docker run --privileged -d -p 4000:5000 --restart=always power-app
